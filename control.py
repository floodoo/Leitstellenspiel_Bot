from data.Emergencies import Emergencies
from data.vehicles import Vehicles
from random import uniform
import threading
from time import sleep
import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import logging


class Control():

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        url = "https://www.leitstellenspiel.de/users/sign_in"

        user = "test-1234"
        pw = "test"
        self.emergency_list = []
        self.use_driver = False
        self.load = True

        self.driver = webdriver.Safari()

        self.use_driver = True
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
        self.use_driver = False

        logging.info("THREAD: update_vehicle_data start")
        threading.Thread(target=self.update_vehicle_data).start()
        logging.info("THREAD: update_active_emergency_list start")
        threading.Thread(target=self.update_active_emergency_list).start()
        logging.info("Method: go_through_emergencies start")
        self.go_through_emergencies()

    def update_vehicle_data(self):
        while True:
            if self.use_driver != True:
                self.use_driver = True
                logging.info("Get Vehicle Api")
                self.vehicle.get_vehicle_api()
                self.use_driver = False

                sleep(uniform(10, 20))

    def update_active_emergency_list(self):
        while True:
            if self.use_driver != True:
                self.use_driver = True
                self.load = True
                logging.info("Get all active Emergency id's")
                self.emergency_list = self.emergencies.get_all_active_Emergencies_id()
                self.use_driver = False
                self.load = False

                sleep(uniform(60, 120))

    def go_through_emergencies(self):
        
        while True:
            
            if self.load == False:
            
                if self.use_driver != True:
                    self.use_driver = True

                    for emergency in self.emergency_list:

                        logging.info("Get required vehicles for " + emergency)
                        self.emergencies.get_required_vehicles(emergency)
                        sleep(uniform(5, 10))

                    self.use_driver = False
                    self.load = True
                
Control()
