import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep


class Active_Emergencies():
    
    def __init__(self, driver):
        self.driver = driver

    def get_all_active_Emergencies_id(self):
        url = "https://www.leitstellenspiel.de/"
        active_emergencies = []

        driver.get(url)
        emergencies = self.driver.find_elements_by_class_name("missionSideBarEntry")

        for i in emergencies:
            active_emergencies.append(i.get_attribute("mission_id"))

        return active_emergencies
