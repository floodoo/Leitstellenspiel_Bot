from data.Emergencies import Emergencies
from data.vehicles import Vehicles
from random import uniform
import threading
from time import sleep
import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import logging
import json
import os


class Control():

    def __init__(self):
        logging.getLogger(__name__)
        logging.basicConfig(format='%(levelname)s-%(message)s', level=logging.INFO)

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

        self.update_vehicle_data()
        threading.Thread(target=self.update_active_emergency_list).start()
        self.update_active_emergency_list()
        self.go_through_emergencies()

    def update_vehicle_data(self):
        if self.use_driver != True:
            self.use_driver = True
            logging.info("Update Vehicles")
            self.vehicle.get_vehicle_api()
            self.use_driver = False

    def update_active_emergency_list(self):
        if self.use_driver != True:
            self.use_driver = True
            self.load = True
            logging.info("Update active emergency list")
            self.emergency_list = self.emergencies.get_all_active_Emergencies_id()
            self.use_driver = False
            self.load = False

    def go_through_emergencies(self):

        while True:

            if self.load == False:

                if self.use_driver != True:
                    self.use_driver = True

                    for emergency in self.emergency_list:

                        logging.info("Update required vehicles for: " + emergency)
                        self.emergencies.get_required_vehicles(emergency)
                        sleep(uniform(5, 10))

                    self.use_driver = False
                    self.send_required_vehicles()
                    sleep(uniform(120, 180))

    def send_required_vehicles(self):
        if self.load == False and self.use_driver == False:
            for mission_id in self.emergency_list:

                logging.info("Current mission ID: " + mission_id)
                with open('required_vehicles_' + mission_id + '.json', 'r') as json_file:
                    obj = json.loads(json_file.read())

                with open('vehicle_data.json', 'r') as vehicle_data_file:
                    vehicle_data = json.loads(
                        vehicle_data_file.read())

                    if int(obj["Benötigte Löschfahrzeuge"]) >= 1:
                        vehicle_number_needet = int(
                            obj["Benötigte Löschfahrzeuge"])
                        counter = 1

                        for i in vehicle_data:
                            if i["vehicle_type"] == 0 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet:
                                counter += 1
                                vehicle_id = i["id"]
                                vehicle_list = []
                                vehicle_list.append(vehicle_id)

                        logging.info("Send vehicles: " + str(vehicle_list))
                        self.emergencies.send_required_vehicles(
                            mission_id, vehicle_list)

                sleep(10)
                logging.debug(
                    "Delete file: required_vehicles_" + mission_id + ".json")
                os.remove("required_vehicles_" + mission_id + ".json")
                logging.debug("Delete file: vehicle_data.json")
                os.remove("vehicle_data.json")
                logging.debug("Rewrite file: vehicle_data.json")
                self.update_vehicle_data()
                sleep(uniform(10, 20))


Control()
