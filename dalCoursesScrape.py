from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
from pprint import pprint
import json


#function definitions

#get the current working directory for file handling
os.getcwd()

#configure webdriver using Chrome Headless and Selenium
option = webdriver.ChromeOptions()
option.add_argument("--headless")

######################################################################################################################
##Enter the course code and description here! This will change what gets scraped.
crn = "PHIL"
faculty = "Philosophy"
######################################################################################################################

driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=option)
driver.get("https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=201910&s_subj=" + crn + "&s_district=100") #navigate to page
driver.implicitly_wait(10)

#driver related vars
coursesTitles = driver.find_elements_by_xpath("//tbody/tr/td[@class='detthdr']/b") #input area
coursesLocations = driver.find_elements_by_xpath("//tbody/tr/td[@class='detthdr']/parent::tr/following-sibling::tr/td[@class='dettl'][13]")
wait = WebDriverWait(driver, 10)



#data related vars



#program execution
out = [x.text for x in coursesTitles]
out2 = [x.text for x in coursesLocations]


courseCodes = []
description = []

#get the course codes and descriptions
for x in out:
    words = x.split()
    code = ' '.join(words[:2])
    desc = ' ' \
           ''.join(words[2:])
    courseCodes.append(code)
    description.append(desc)

#get the campus and building
campus = []
building = []
roomNumber = []
for x in out2:
    words = x.split()
    site = ' '.join(words[:1])
    build = ' '.join(words[1:])
    #split the building from the room number
    secondSplit = build.split()
    i = len(secondSplit)
    build = ' '.join(secondSplit[:(i-1)])
    room = ' '.join(secondSplit[(i-1):])
    campus.append(site)
    building.append(build)
    roomNumber.append(room)

#put all the info into a list of dictionaries
courses = {faculty: {courseCodes[i]:{"description": description[i],
              "campus": campus[i], "building": building[i], "room": roomNumber[i]} for i in range(len(courseCodes))}}

#write the info to JSON format, dump to a file
with open("courses.json", 'a') as file:
    file.write("\n")
    json.dump(courses, file)

#print just to show you it worked
pprint(courses)
print("done")
driver.quit()
