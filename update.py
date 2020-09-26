#selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
from datetime import datetime

import signal
import sys

#sqlite import
import sqlite3

#sendgrid imports
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def handler(signum, frame):
    print("Quitting time")
    cur.close()
    driver.quit()

signal.signal(signal.SIGINT, handler)

def send_email_update():
    message = Mail(
        from_email='maf946@psu.edu',
        to_emails='mfriedenberg@gmail.com',
        subject=' PSU Covid Dashboard Update',
        html_content='New overall total positive number: ' + str(overall_total_positive))
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

print("Starting up…")

# create a database connection
conn = create_connection()
cur = conn.cursor()

driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
url ='https://app.powerbi.com/view?r=eyJrIjoiMDFhMzI2YzQtNmQwNC00YjgzLWFjMzAtZmFlNGQyZGZiZGJhIiwidCI6IjdjZjQ4ZDQ1LTNkZGItNDM4OS1hOWMxLWMxMTU1MjZlYjUyZSIsImMiOjF9'

while 1:
    if (datetime.today().weekday() == 1 or datetime.today().weekday() == 4): #check if today is Tuesday or Friday
        query_string = "select overall_total_positive from covid_data order by update_time desc limit 1"
        last_recorded_overall_total_positive = int(cur.execute(query_string).fetchone()[0])

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

            ####
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

            #overall_total_positive = overall_total_positive + 1 # DEBUG LINE, TO TEST FOR WHEN THERE ARE UPDATES

            if (overall_total_positive != last_recorded_overall_total_positive):
                print("There has been a change")
                print("Overall total positive: ", overall_total_positive)
                print("Last recorded: ", last_recorded_overall_total_positive)
                update_database()
                send_email_update()
                print_updated_numbers()
            else:
                now = datetime.now()
                dt_string = now.strftime("%Y-%m-%d %I:%M:%S %p:")
                print (dt_string, "No change in the recorded numbers")
        except Exception as e:
            print("I hit an error", e)
        time.sleep(30)



