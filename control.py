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

        user = ""
        pw = ""
        self.emergency_list = []

        self.driver = webdriver.Safari()
        self.driver.get(url)

        username = self.driver.find_element_by_id("user_email")
        password = self.driver.find_element_by_id("user_password")

        username.send_keys(user)
        password.send_keys(pw)

        self.driver.find_element_by_name("commit").click()

        sleep(uniform(2, 3))
        self.driver.find_element_by_class_name("cookies-eu-ok").click()
        
        self.emergencies = Emergencies(self.driver)
        self.vehicle = Vehicles(self.driver)

        threading.Thread(target=self.update_vehicle_data).start()
        threading.Thread(target=self.update_active_emergency_list).start()
        self.go_through_emergencies()

    def update_vehicle_data(self):
        while True:
            self.vehicle.get_vehicle_api()
            sleep(uniform(10, 20))
            
    def update_active_emergency_list(self):
        while True:
            self.emergency_list = self.emergencies.get_all_active_Emergencies_id()
            sleep(uniform(50, 80))
            
    def go_through_emergencies(self):
        
        for emergency in self.emergency_list:
            self.emergencies.get_required_vehicles(emergency)
            sleep(uniform(5, 10))

Control()
