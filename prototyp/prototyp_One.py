import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep

url = "https://www.leitstellenspiel.de/users/sign_in"
user = ""
pw = ""
active_emergencies = []

driver = webdriver.Safari()
driver.maximize_window()

driver.get(url)

username = driver.find_element_by_id("user_email")
password = driver.find_element_by_id("user_password")

username.send_keys(user)
password.send_keys(pw)

driver.find_element_by_name("commit").click()

sleep(2)
driver.find_element_by_class_name("cookies-eu-ok").click()

emergencies = driver.find_elements_by_class_name("missionSideBarEntry")

for i in emergencies:
    print("Active emergency: " + i.text)
    active_emergencies.append(i.get_attribute("id"))
    
    
driver.quit()
