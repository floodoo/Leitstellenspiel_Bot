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

    def get_required_vehicles(self):
        url = "https://www.leitstellenspiel.de/missions/1838186552"

        self.driver.get(url)
        sleep(2)
        self.driver.find_element_by_id("navbar-right-help-button").click()
        sleep(1)
        test = self.driver.find_elements_by_class_name("table-striped")[1]
        vehicles_needet = test.text

        vehicles_needet = os.linesep.join(
            [s for s in vehicles_needet.splitlines() if s.strip()])

        with open("test.txt", "w") as text_file:
            text_file.write(vehicles_needet)
            text_file.close()

        with open("test.txt", "r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if "Beschreibung" not in line and "Wert" not in line:
                    f.write(line)
            f.truncate()
        counter = 0
        second_counter = 0
        
        num_lines = sum(1 for line in open('test.txt'))
        num_lines -= 1
        
        with open('test.txt', 'r') as f, open('required_vehicles.json', 'w') as fo:
            fo.write("{")
                
            for line in f:
                durchZwei = counter % 2
                
                if counter == num_lines:
                    fo.write(line.strip() + '"\n')
                    print("counter == num_lines")
                
                elif durchZwei != 0:
                    fo.write(line.strip() + '",\n')
                    print("normal")
                    
                else:
                    fo.write('"' + line.strip() + '":"')
                    print(": gesetzt")
                    
                counter += 1
                    
            fo.write("}")
                    
        driver.quit()


url = "https://www.leitstellenspiel.de/users/sign_in"
user = ""
pw = ""

driver = webdriver.Safari()
# driver.maximize_window()

driver.get(url)

username = driver.find_element_by_id("user_email")
password = driver.find_element_by_id("user_password")

username.send_keys(user)
password.send_keys(pw)

driver.find_element_by_name("commit").click()

sleep(3)
driver.find_element_by_class_name("cookies-eu-ok").click()

test = Emergencies(driver)
test.get_required_vehicles()
