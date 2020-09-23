from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sqlite3
from sqlite3 import Error

##TODO the sqlite stuff doesn't work at all

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
url ='https://app.powerbi.com/view?r=eyJrIjoiMDFhMzI2YzQtNmQwNC00YjgzLWFjMzAtZmFlNGQyZGZiZGJhIiwidCI6IjdjZjQ4ZDQ1LTNkZGItNDM4OS1hOWMxLWMxMTU1MjZlYjUyZSIsImMiOjF9'
driver.get(url)
time.sleep(5)

iframe_list =  driver.find_elements_by_tag_name("iframe")

number_list = []
for i in iframe_list:
    driver.switch_to.frame(i)
    text_list = driver.find_elements_by_tag_name("text")
    number_list.append(text_list[0].text.replace(',', '')) #remove commas, as in the case of "1,335 cases"
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

def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect('psu_covid_dash_checker.sqlite3')
        print(sqlite3.version)
    except:
        print ("error connecting to db")
    return conn


# create a database connection
conn = create_connection()

cur = conn.cursor()
insert_string = "INSERT INTO covid_data (overall_total_positive, overall_current_active, overall_cases_no_longer_active,  overall_persons_currently_in_quarantine, overall_persons_currently_in_isolation, ondemand_total_tests_performed, ondemand_total_positive_cases, ondemand_total_awaiting_results, random_total_tests_performed, random_total_positive_cases, random_total_awaiting_results) VALUES ("
insert_string += overall_total_positive + ", "
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
cur.close()

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