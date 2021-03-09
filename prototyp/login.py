import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep

url = "https://www.leitstellenspiel.de/users/sign_in"
user = ""
pw = ""


browser = webdriver.Safari()
browser.get(url)

username = browser.find_element_by_id("user_email")
password = browser.find_element_by_id("user_password")

username.send_keys(user)
password.send_keys(pw)

browser.find_element_by_name("commit").click()

sleep(3)
browser.find_element_by_class_name("cookies-eu-ok").click()

sleep(2)
browser.quit()
