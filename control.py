from data.Emergencies import Emergencies
from data.vehicles import Vehicles
from random import uniform
import threading
from time import sleep
import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class Control():

    def __init__(self):
        url = "https://www.leitstellenspiel.de/users/sign_in"

        user = "Flo0705"
        pw = "Xx66q3we"

        self.driver = webdriver.Safari()
        self.driver.get(url)

        username = self.driver.find_element_by_id("user_email")
        password = self.driver.find_element_by_id("user_password")

        username.send_keys(user)
        password.send_keys(pw)

        self.driver.find_element_by_name("commit").click()

        sleep(uniform(1.5, 2.5))
        self.driver.find_element_by_class_name("cookies-eu-ok").click()
        
        thread = threading.Thread(target=self.update_vehicle_data)
        thread.start()

    def update_vehicle_data(self):
        vehicle = Vehicles(self.driver)
        vehicle.get_vehicle_api()
        sleep(uniform(10, 20))

Control()