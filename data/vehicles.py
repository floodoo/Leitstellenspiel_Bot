import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep


class Vehicles():

    def __init__(self, driver):
        self.driver = driver

    def get_all_vehicle_id(self):
        url = "https://www.leitstellenspiel.de/vehicles/"
        all_vehicles = []

        driver.get(url)
        vehicles = self.driver.find_elements_by_xpath(
            "//a[contains(@href,'vehicles')]")
        
        for i in vehicles:
            all_vehicles.append(i.get_attribute("href")[41:])
        
        return all_vehicles

    def get_all_vehicle_types(self):
        url = "https://www.leitstellenspiel.de/vehicles/"
        all_vehicle_types = []

        driver.get(url)
        vehicles = self.driver.find_elements_by_class_name(
            "vehicle_image_reload")
        
        for i in vehicles:
            all_vehicle_types.append(i.get_attribute("vehicle_type_id"))
            
        return all_vehicle_types
   
   
   
        
url = "https://www.leitstellenspiel.de/users/sign_in"
user = ""
pw = ""

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

test = Vehicles(driver)
print(test.get_all_vehicle_id())
print(test.get_all_vehicle_types())