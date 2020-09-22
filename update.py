from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

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

print("## Overall Numbers")
print("")
print ("Total Positive Cases: ", number_list[10])
print ("Current Active Cases: ", number_list[12])
print ("Cases No Longer Active: ", number_list[11])
print("")
print ("Persons Currently in Quarantine: ", number_list[7])
print ("Persons Currently in Isolation: ", number_list[8])
print("")
print ("## On-Demand Testing")
print("")
print ("Total Tests Performed: ", number_list[2])
print ("Total Positive Cases: ", number_list[1])
print ("Total Awaiting Results: ", number_list[0])
print("")
print ("## Random Testing")
print("")
print ("Total Tests Performed: ", number_list[5])
print ("Total Positive Cases: ", number_list[4])
print ("Total Awaiting Results: ", number_list[3])