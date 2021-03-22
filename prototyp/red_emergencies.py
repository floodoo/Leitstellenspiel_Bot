import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import json


url = "https://www.leitstellenspiel.de/users/sign_in"
user = "test-1234"
pw = "test"

driver = webdriver.Safari()

driver.get(url)

username = driver.find_element_by_id("user_email")
password = driver.find_element_by_id("user_password")

username.send_keys(user)
password.send_keys(pw)

driver.find_element_by_name("commit").click()

sleep(2)
driver.find_element_by_class_name("cookies-eu-ok").click()
sleep(2)

active_emergencies = []

emergencies = driver.find_elements_by_class_name(
    "mission_panel_red")

for i in emergencies:
    mission_id = i.get_attribute("id")
    active_emergencies.append(mission_id[14:])

print(active_emergencies)
print("Done")
