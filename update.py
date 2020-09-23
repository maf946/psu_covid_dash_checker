from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sqlite3

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path='/Users/marc/chromedriver', options=options)
url ='https://app.powerbi.com/view?r=eyJrIjoiMDFhMzI2YzQtNmQwNC00YjgzLWFjMzAtZmFlNGQyZGZiZGJhIiwidCI6IjdjZjQ4ZDQ1LTNkZGItNDM4OS1hOWMxLWMxMTU1MjZlYjUyZSIsImMiOjF9'
driver.get(url)
time.sleep(5)

iframe_list =  driver.find_elements_by_tag_name("iframe")

number_list = []
for i in iframe_list:
    driver.switch_to.frame(i)
    text_list = driver.find_elements_by_tag_name("text")
    number_list.append(text_list[0].text)
    time.sleep(.25)
    driver.switch_to.default_content()
driver.quit()

overall_total_positive = number_list[10]
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

conn = sqlite3.connect('psu_covid_dash_checker.sqlite3')
c = conn.cursor()
insert_string = "INSERT INTO covid_data (overall_total_positive, overall_current_active, overall_cases_no_longer_active,  overall_persons_currently_in_quarantine, overall_persons_currently_in_isolation, ondemand_total_tests_performed, ondemand_total_positive_cases, ondemand_total_awaiting_results, random_total_tests_performed, random_total_positive_cases, random_total_awaiting_results) " \
                "VALUES (overall_total_positive, overall_current_active, overall_cases_no_longer_active,  overall_persons_currently_in_quarantine, overall_persons_currently_in_isolation, ondemand_total_tests_performed, ondemand_total_positive_cases, ondemand_total_awaiting_results, random_total_tests_performed, random_total_positive_cases, random_total_awaiting_results);"

print(insert_string)
#c.execute(insert_string)

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