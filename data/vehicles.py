import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import json


class Vehicles():

    def __init__(self, driver):
        self.driver = driver

    # def get_all_vehicle_id(self):
    #     url = "https://www.leitstellenspiel.de/vehicles/"
    #     all_vehicle_id = []

    #     self.driver.get(url)
    #     vehicles = self.driver.find_elements_by_xpath(
    #         "//a[contains(@href,'vehicles')]")
        
    #     for i in vehicles:
    #         all_vehicle_id.append(i.get_attribute("href")[41:])
        
    #     return all_vehicle_id

    # def get_all_vehicle_types(self):
    #     url = "https://www.leitstellenspiel.de/vehicles/"
    #     all_vehicle_types = []

    #     self.driver.get(url)
    #     vehicles = self.driver.find_elements_by_class_name(
    #         "vehicle_image_reload")
        
    #     for i in vehicles:
    #         all_vehicle_types.append(i.get_attribute("vehicle_type_id"))
            
    #     return all_vehicle_types
   
    # The simple version did not work
    def get_vehicle_api(self):
        url = "https://www.leitstellenspiel.de/api/vehicles"
       
        self.driver.get(url)
        json_data = self.driver.find_element_by_xpath("/html/body/pre")
        json_data = json_data.text
        
        with open("data.json", "w") as json_file:
            json.dump(json_data, json_file)
            json_file.close()
            
        # Remove Backslash and "
        with open("data.json", "r") as json_file:
            filedata = json_file.read()
            filedata = filedata.replace("\\", "")
            filedata = filedata[1:-1]
            json_file.close()

        with open("data.json", "w") as json_file:
            json_file.write(filedata)
            json_file.close()
        
        # Beautify Json File
        with open('data.json') as json_file:
            obj = json.load(json_file)
            outfile = open('data.json', "w")
            outfile.write(json.dumps(obj, indent=4, sort_keys=True))
            outfile.close()
        
        driver.close()
        
        
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
test.get_vehicle_api()
