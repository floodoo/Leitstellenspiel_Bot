import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import json


class Vehicles():
    
    def __init__(self, driver):
        self.driver = driver
        self.filename = "data.json"
   
    # The simple version did not work
    def get_vehicle_api(self):
        url = "https://www.leitstellenspiel.de/api/vehicles"
       
        self.driver.get(url)
        json_data = self.driver.find_element_by_xpath("/html/body/pre")
        json_data = json_data.text
        
        with open(self.filename, "w") as json_file:
            json.dump(json_data, json_file)
            json_file.close()
            
        # Remove Backslash and "
        with open(self.filename, "r") as json_file:
            filedata = json_file.read()
            filedata = filedata.replace("\\", "")
            filedata = filedata[1:-1]
            json_file.close()

        with open(self.filename, "w") as json_file:
            json_file.write(filedata)
            json_file.close()
        
        # Beautify Json File
        with open(self.filename) as json_file:
            obj = json.load(json_file)
            outfile = open(self.filename, "w")
            outfile.write(json.dumps(obj, indent=4, sort_keys=True))
            outfile.close()
        
    def get_all_vehicle_id(self):
        all_vehicle_id = []

        with open(self.filename, "r") as json_file:
            data = json.load(json_file)
            for i in data:
                all_vehicle_id.append(i["id"])
                
            json_file.close()
            
            return all_vehicle_id
        
    def get_all_vehicle_types(self):
        all_vehicle_types = []

        with open(self.filename, "r") as json_file:
            data = json.load(json_file)
            for i in data:
                all_vehicle_types.append(i["vehicle_type"])

            json_file.close()

            return all_vehicle_types
        
    def get_all_vehicle_fms_real(self):
        all_vehicle_fms_real = []

        with open(self.filename, "r") as json_file:
            data = json.load(json_file)
            for i in data:
                all_vehicle_fms_real.append(i["fms_real"])

            json_file.close()

            return all_vehicle_fms_real
        
    def get_all_vehicle_fms_show(self):
        all_vehicle_fms_show = []

        with open(self.filename, "r") as json_file:
            data = json.load(json_file)
            for i in data:
                all_vehicle_fms_show.append(i["fms_show"])

            json_file.close()

            return all_vehicle_fms_show
        
    def get_all_vehicle_target_type(self):
        all_vehicle_target_type = []

        with open(self.filename, "r") as json_file:
            data = json.load(json_file)
            for i in data:
                all_vehicle_target_type.append(i["target_type"])

            json_file.close()

            return all_vehicle_target_type
        
    def get_all_vehicle_target_id(self):
        all_vehicle_target_id = []

        with open(self.filename, "r") as json_file:
            data = json.load(json_file)
            for i in data:
                all_vehicle_target_id.append(i["target_id"])

            json_file.close()

            return all_vehicle_target_id
        
    def get_all_vehicle_building_id(self):
        all_vehicle_building_id = []

        with open(self.filename, "r") as json_file:
            data = json.load(json_file)
            for i in data:
                all_vehicle_building_id.append(i["building_id"])

            json_file.close()

            return all_vehicle_building_id
        
    def get_all_vehicle_caption(self):
        all_vehicle_caption = []

        with open(self.filename, "r") as json_file:
            data = json.load(json_file)
            for i in data:
                all_vehicle_caption.append(i["caption"])

            json_file.close()

            return all_vehicle_caption