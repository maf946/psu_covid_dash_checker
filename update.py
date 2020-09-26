#selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

executable_path = './chromedriver'

import time
from datetime import datetime

import signal

import argparse

from colorama import Fore, Back, Style

#sqlite import
import sqlite3

#sendgrid imports
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import random

import sys

def handler(signum, frame):
    print("Quitting time")
    cur.close()
    driver.quit()

signal.signal(signal.SIGINT, handler)

def send_email_update():
    from_email = 'maf946@psu.edu'
    to_email = 'mfriedenberg@gmail.com'
    subject = 'PSU Covid Dashboard Update: ' + str(overall_total_positive)
    if (test_mode):
        subject = "TEST MODE: " + subject
    html_content='See <a href=\"' + url + '\">complete dashboard</a> for more information.'

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e.message)

def update_database():
    insert_string = "INSERT INTO covid_data (overall_total_positive, overall_current_active, overall_cases_no_longer_active,  overall_persons_currently_in_quarantine, overall_persons_currently_in_isolation, ondemand_total_tests_performed, ondemand_total_positive_cases, ondemand_total_awaiting_results, random_total_tests_performed, random_total_positive_cases, random_total_awaiting_results) VALUES ("
    insert_string += str(overall_total_positive) + ", "
    insert_string += overall_current_active + ", "
    insert_string += overall_cases_no_longer_active + ", "
    insert_string += overall_persons_currently_in_quarantine + ", "
    insert_string += overall_persons_currently_in_isolation + ", "
    insert_string += ondemand_total_tests_performed + ", "
    insert_string += ondemand_total_positive_cases + ", "
    insert_string += ondemand_total_awaiting_results + ", "
    insert_string += random_total_tests_performed + ", "
    insert_string += random_total_positive_cases + ", "
    insert_string += random_total_awaiting_results + ");"
    cur.execute(insert_string)
    conn.commit()

def print_updated_numbers():
    print("## Overall Numbers")
    print("")
    print ("Total Positive Cases: ", overall_total_positive)
    print ("Current Active Cases: ", overall_current_active)
    print ("Cases No Longer Active: ", overall_cases_no_longer_active)
    print("")
    print ("Persons Currently in Quarantine: ", overall_persons_currently_in_quarantine)
    print ("Persons Currently in Isolation: ", overall_persons_currently_in_isolation)
    print("")
    print ("## On-Demand Testing")
    print("")
    print ("Total Tests Performed: ", ondemand_total_tests_performed)
    print ("Total Positive Cases: ", ondemand_total_positive_cases)
    print ("Total Awaiting Results: ", ondemand_total_awaiting_results)
    print("")
    print ("## Random Testing")
    print("")
    print ("Total Tests Performed: ", random_total_tests_performed)
    print ("Total Positive Cases: ", random_total_positive_cases)
    print ("Total Awaiting Results: ", random_total_awaiting_results)

def create_connection():
    # create a database connection to a SQLite database
    conn = None
    try:
        conn = sqlite3.connect('psu_covid_dash_checker.sqlite3')
    except:
        print ("error connecting to db")
    return conn

options = Options()
options.headless = True


parser = argparse.ArgumentParser(description='Start up a tool that checks for updates to the PSU COVID Dashboard.')
parser.add_argument("--test-mode", default=False, action="store_true" , help="Generate a random value for overall_total_positive, and send an email, but do not update database")
args = parser.parse_args()
test_mode = args.test_mode

if (test_mode):
    sys.stdout.write(Fore.RED + Back.BLACK + Style.BRIGHT + '\n*** Running in test mode ***\n')
    print(Style.RESET_ALL)

# create a database connection
conn = create_connection()
cur = conn.cursor()

url ='https://app.powerbi.com/view?r=eyJrIjoiMDFhMzI2YzQtNmQwNC00YjgzLWFjMzAtZmFlNGQyZGZiZGJhIiwidCI6IjdjZjQ4ZDQ1LTNkZGItNDM4OS1hOWMxLWMxMTU1MjZlYjUyZSIsImMiOjF9'

loop_number = 0

while 1:
    loop_number = loop_number + 1
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %I:%M:%S %p")

    query_string = "select overall_total_positive from covid_data order by update_time desc limit 1"
    last_recorded_overall_total_positive = int(cur.execute(query_string).fetchone()[0])


    driver = webdriver.Chrome(executable_path=executable_path, options=options)
    driver.get(url)
    time.sleep(5)

    iframe_list =  driver.find_elements_by_tag_name("iframe")

    try:
        number_list = []
        for i in iframe_list:
            driver.switch_to.frame(i)
            text_list = driver.find_elements_by_tag_name("text")
            number_list.append(text_list[0].text.replace(',', '')) #remove commas, as in the case of "1,335 cases"
            time.sleep(.25)
            driver.switch_to.default_content()

        driver.quit()
        overall_total_positive = int(number_list[10])
        overall_current_active = number_list[12]
        overall_cases_no_longer_active = number_list[11]
        overall_persons_currently_in_quarantine = number_list[7]
        overall_persons_currently_in_isolation = number_list[8]
        ondemand_total_tests_performed = number_list[2]
        ondemand_total_positive_cases = number_list[1]
        ondemand_total_awaiting_results = number_list[0]
        random_total_tests_performed = number_list[5]
        random_total_positive_cases = number_list[4]
        random_total_awaiting_results = number_list[3]

        if (test_mode):
            overall_total_positive = random.randint(1000000000,9999999999)

        if (overall_total_positive != last_recorded_overall_total_positive):
            print("Overall total positive: ", overall_total_positive)
            print("Last recorded: ", last_recorded_overall_total_positive)
            if (not test_mode):
                update_database()
            send_email_update()
            print_updated_numbers()
        else:
            if (datetime.today().weekday() == 1 or datetime.today().weekday() == 4): #check if today is Tuesday or Friday
                sys.stdout.write('%s (loop number %s): overall_total_positive is still %s.\r' % (dt_string, str(loop_number), overall_total_positive))
                sys.stdout.flush()
            else:
                sys.stdout.write('%s (loop number %s): overall_total_positive is still %s. It\'s not dashboard update day; waiting 2 minutes.\r' % (dt_string, str(loop_number), overall_total_positive))
                sys.stdout.flush()
                time.sleep(120)

    except Exception as e:
        sys.stdout.write(Fore.RED + Back.BLACK + Style.BRIGHT + '%s: I hit an error: %s' % (dt_string, e))
        print(Style.RESET_ALL)




