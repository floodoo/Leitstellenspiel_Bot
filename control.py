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
        logging.basicConfig(
            format='%(levelname)s-%(message)s', level=logging.INFO)

        url = "https://www.leitstellenspiel.de/users/sign_in"

        user = "test-1234"
        pw = "test"
        self.emergency_list = []
        self.use_driver = False
        self.load = True
        self.benoetigte_Fahrzeuge = [
            "Benötigte Löschfahrzeuge", "Benötigte Streifenwagen"]
        self.LF_list = [0, 1, 6, 7, 8, 9, 30, 37,
                        17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        self.GWS_list = [11, 13, 14, 15, 16]
        self.RW_list = [4, 30]

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

    def update_vehicle_data(self):
        if self.use_driver != True:
            self.use_driver = True
            logging.info("Update Vehicles")
            self.vehicle.get_vehicle_api()
            self.use_driver = False
            sleep(uniform(1, 5))

    def update_active_emergency_list(self):
        while True:
            if self.use_driver != True:
                self.use_driver = True
                self.load = True
                self.emergency_list = []
                logging.info("Update active emergency list")
                self.emergency_list = self.emergencies.get_all_active_Emergencies_id()
                logging.info("Active Emergencies: " + str(self.emergency_list))
                self.use_driver = False
                self.load = False
                self.go_through_emergencies()
                sleep_time = uniform(180, 240)
                print("Waiting.... " + str(sleep_time))
                url = "https://www.leitstellenspiel.de/"
                self.driver.get(url)
                sleep(sleep_time)

    def go_through_emergencies(self):
        end = False
        while end != True:

            if self.load == False:

                if self.use_driver != True:
                    self.use_driver = True

                    for emergency in self.emergency_list:

                        logging.info(
                            "Update required vehicles for: " + emergency)
                        self.emergencies.get_required_vehicles(emergency)
                        sleep(uniform(5, 10))

                    self.use_driver = False
                    self.send_required_vehicles()
                    end = True

    def send_required_vehicles(self):
        end = False
        while end != True:
            if self.load == False and self.use_driver == False:
                for mission_id in self.emergency_list:
                    self.update_vehicle_data()

                    logging.info("Current mission ID: " + mission_id)
                    with open('required_vehicles_' + mission_id + '.json', 'r') as json_file:
                        obj = json.loads(json_file.read())

                    with open('vehicle_data.json', 'r') as vehicle_data_file:
                        vehicle_data = json.loads(
                            vehicle_data_file.read())

                    vehicle_list = []
                    not_enough_vehicles = False

                    for benoetigt in self.benoetigte_Fahrzeuge:

                        if benoetigt in obj:
                            vehicle_number_needet = int(
                                obj[benoetigt])

                            counter = 1

                            if benoetigt == "Benötigte ELW 1":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 3 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 3 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte ELW 2":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 34 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 34 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte Löschfahrzeuge":

                                for i in vehicle_data:
                                    if i["vehicle_type"] in self.LF_list and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] in self.LF_list and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte Drehleitern":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 2 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 2 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte Rüstwagen":

                                for i in vehicle_data:
                                    if i["vehicle_type"] in self.RW_list and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] in self.RW_list and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte GW-A":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 5 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 5 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte GW-Öl":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 10 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 10 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte GW-Gefahrgut":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 27 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 27 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte GW-Höhenrettung":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 33 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 33 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte GW-Mess":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 12 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 12 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte GW L 2 Wasser":

                                for i in vehicle_data:
                                    if i["vehicle_type"] in self.GWS_list and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] in self.GWS_list and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte Dekon-P":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 53 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 53 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte Streifenwagen":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 32 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 32 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte leBefKw":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 35 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 35 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte GruKw":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 50 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 50 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte FüKw":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 51 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 51 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte GefKw":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 52 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 52 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            elif benoetigt == "Benötigte GefKw":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 52 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 52 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)
                                        
                            elif benoetigt == "Benötigte GKW":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 39 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 30 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)
                                        
                            elif benoetigt == "Benötigte MTW-TZ":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 40 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 40 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)
                                        
                            elif benoetigt == "Benötigte MzKW":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 41 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 41 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)
                                        
                            elif benoetigt == "Benötigte LKW K 9":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 42 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 42 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)
                                        
                            elif benoetigt == "Benötigte BRmG R":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 43 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 43 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)
                                        
                            elif benoetigt == "Benötigte Anh DLE":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 44 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 44 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)
                                        
                            elif benoetigt == "Benötigte MLW 5":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 45 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 45 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)
                                        
                            elif benoetigt == "Benötigte FwK":

                                for i in vehicle_data:
                                    if i["vehicle_type"] == 57 and i["fms_show"] == 2 and i["fms_real"] == 2 and counter <= vehicle_number_needet or i["vehicle_type"] == 57 and i["fms_show"] == 1 and i["fms_real"] == 1 and counter <= vehicle_number_needet:
                                        counter += 1
                                        vehicle_id = i["id"]
                                        vehicle_list.append(vehicle_id)

                            else:
                                not_enough_vehicles = True
                                print("No free vehicles")

                    if not_enough_vehicles != True:

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

                print("Done.....")

            end = True
