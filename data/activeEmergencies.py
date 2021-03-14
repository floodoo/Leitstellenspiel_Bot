import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import os
import json


class Emergencies():

    def __init__(self, driver):
        self.driver = driver

    def get_all_active_Emergencies_id(self):
        url = "https://www.leitstellenspiel.de/"
        active_emergencies = []

        self.driver.get(url)
        emergencies = self.driver.find_elements_by_class_name(
            "missionSideBarEntry")

        for i in emergencies:
            active_emergencies.append(i.get_attribute("mission_id"))

        return active_emergencies

    def get_required_vehicles(self, mission_id):
        url = "https://www.leitstellenspiel.de/missions/" + mission_id

        self.driver.get(url)
        sleep(2)
        self.driver.find_element_by_id("navbar-right-help-button").click()
        sleep(1)
        test = self.driver.find_elements_by_class_name("table-striped")[1]
        vehicles_needet = test.text

        vehicles_needet = os.linesep.join(
            [s for s in vehicles_needet.splitlines() if s.strip()])

        with open("required_vehicles.txt", "w") as text_file:
            text_file.write(vehicles_needet)
            text_file.close()

        with open("required_vehicles.txt", "r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if "Beschreibung" not in line and "Wert" not in line:
                    f.write(line)
            f.truncate()
        counter = 0
        second_counter = 0
        
        num_lines = sum(1 for line in open('required_vehicles.txt'))
        num_lines -= 1
        
        with open('required_vehicles.txt', 'r') as f, open('required_vehicles.json', 'w') as fo:
            fo.write("{")
                
            for line in f:
                durchZwei = counter % 2
                
                if counter == num_lines:
                    fo.write(line.strip() + '"\n')
                
                elif durchZwei != 0:
                    fo.write(line.strip() + '",\n')
                    
                else:
                    fo.write('"' + line.strip() + '":"')
                    
                counter += 1
                    
            fo.write("}")