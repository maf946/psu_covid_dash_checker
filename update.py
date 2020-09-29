# TODO: sqlite: include statements to create the table IF NOT EXISTS
# TODO: fix so you can run both test-mode and run-once

from emailFunctions import *
from databaseFunctions import *
from printFunctions import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
from datetime import datetime

import signal


import argparse

from colorama import Fore, Back, Style

import random

import sys


def handler(_, __):
    print("\nGoodbye")
    driver.quit()
    quit()


signal.signal(signal.SIGINT, handler)

options = Options()
options.headless = True
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
options.add_experimental_option("prefs", {"managed_default_content_settings.stylesheets": 2})
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.plugins": 2})
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.popups": 2})
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.geolocation": 2})
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.media_stream": 2})

parser = argparse.ArgumentParser(description='Start up a tool that checks for updates to the PSU COVID Dashboard.')
parser.add_argument("--test-mode", default=False, action="store_true",
                    help="Generate a random value for overall_total_positive, "
                         "and send an email, but do not update database")
parser.add_argument("--run-once", default=False, action="store_true",
                    help="Run one time, then quit. In other words, don't loop")
parser.add_argument("--chromedriver-path", "-driverpath", default='./chromedriver', help="location of chromedriver")
parser.add_argument("--sendgrid-api-key-file", "-sendgrid-key-file", default='../sendgrid_api_key_file',
                    help="location of file containing sendgrid api key")
args = parser.parse_args()
test_mode = args.test_mode
run_once = args.run_once
driverpath = args.chromedriver_path
sendgrid_api_key_file = args.sendgrid_api_key_file
sendgrid_api_key = ''

start_time = time.time()

try:
    f = open(sendgrid_api_key_file, "r")
    sendgrid_api_key = f.read()
    f.close()
except IOError:
    print("Could not find sendgrid_api_key. Quitting.")
    quit()

if test_mode:
    sys.stdout.write(Fore.RED + Back.BLACK + Style.BRIGHT + '*** Running in test mode ***')
    print(Style.RESET_ALL)

if run_once:
    sys.stdout.write(Fore.RED + Back.BLACK + Style.BRIGHT + '*** Just running once ***')
    print(Style.RESET_ALL)

loop_number = 0

while 1:
    loop_number = loop_number + 1
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %I:%M:%S %p")

    last_recorded_overall_total_positive = get_last_recorded_overall_total_positive()

    try:
        driver = webdriver.Chrome(executable_path=driverpath, options=options)
        driver.get(settings.url)
        time.sleep(5)

        iframe_list = driver.find_elements_by_tag_name("iframe")
        number_list = []
        for i in iframe_list:
            driver.switch_to.frame(i)
            text_list = driver.find_elements_by_tag_name("text")
            try:
                number_list.append(text_list[0].text.replace(',', ''))  # remove commas, as in the case of "1,335 cases"
            except IndexError:
                number_list.append("fail")
                print("Hit failure here.")

            time.sleep(.1)
            driver.switch_to.default_content()

        driver.save_screenshot("screenshot.png")
        driver.close()
        driver.quit()

        dataDictionary = dict()
        dataDictionary['overall_total_positive'] = int(number_list[10])
        dataDictionary['overall_current_active'] = int(number_list[12])
        dataDictionary['overall_cases_no_longer_active'] = int(number_list[11])
        dataDictionary['overall_persons_currently_in_quarantine'] = int(number_list[7])
        dataDictionary['overall_persons_currently_in_isolation'] = int(number_list[8])
        dataDictionary['ondemand_total_tests_performed'] = int(number_list[2])
        dataDictionary['ondemand_total_positive_cases'] = int(number_list[1])
        dataDictionary['ondemand_total_awaiting_results'] = int(number_list[0])
        dataDictionary['random_total_tests_performed'] = int(number_list[5])
        dataDictionary['random_total_positive_cases'] = int(number_list[4])
        dataDictionary['random_total_awaiting_results'] = int(number_list[3])

        if test_mode:
            dataDictionary['overall_total_positive'] = random.randint(1000000000, 9999999999)

        if dataDictionary['overall_total_positive'] != last_recorded_overall_total_positive:
            print("Overall total positive: ", dataDictionary['overall_total_positive'])
            print("Last recorded: ", last_recorded_overall_total_positive)
            if not test_mode:
                update_database(dataDictionary)
            send_email_update(test_mode, dataDictionary['overall_total_positive'], sendgrid_api_key)
            print_updated_numbers(dataDictionary)
        else:
            elapsed_time = time.time() - start_time
            time_per_loop = elapsed_time / loop_number
            sys.stdout.write('%s: overall_total_positive is still %s (loop number %s; %is per loop)\r' % (
                dt_string, dataDictionary['overall_total_positive'], str(loop_number), time_per_loop))
            sys.stdout.flush()
            if run_once:
                print("\nGoodbye.")
                break
    except Exception as e:
        sys.stdout.write(Fore.RED + Back.BLACK + Style.BRIGHT + '%s: I hit an error: %s ' % (
            dt_string, e))
        time.sleep(30)
        print(Style.RESET_ALL)
