from selenium import webdriver
import requests
import time
import sys
import shutil
import os
import json

# Constants to find out current Operating System and Working Directory
CURRENT_OS = sys.platform
CURRENT_DIRECTORY = os.getcwd()


def pre_checks_os(operating_system, current_directory):
    # Checks if OS is a Linux System and moves the according webdriver for Selenium
    # to the current working directory
    if operating_system == "linux":
        if os.path.exists(current_directory + "/geckodriver") is False:
            shutil.move(
                current_directory + "/webdrivers/geckodriver_linux64",
                current_directory + "/geckodriver",
            )
        time.sleep(5)
        # Checks whether CSV file already exists, otherwise creates one
        if os.path.exists(current_directory + "/prices.csv") is False:
            csv_file = open("prices.csv", "a")
            csv_file.write("Time,Low Price,High Price\n")

    # Same as above, just for a Windows System
    if operating_system == "windows":
        if os.path.exists(current_directory + "\geckodriver.exe") is False:
            shutil.move(
                current_directory + "\webdrivers\geckodriver_win64.exe",
                current_directory + "\geckodriver.exe",
            )
        time.sleep(5)
        # Checks whether CSV file already exists, otherwise creates one
        if os.path.exists(current_directory + "\prices.csv") is False:
            csv_file = open("prices.csv", "a")
            csv_file.write("Time,Low Price,High Price\n")


pre_checks_os(CURRENT_OS, CURRENT_DIRECTORY)

# Defines which browser will be used to open website with Selenium
browser = webdriver.Firefox(executable_path=CURRENT_DIRECTORY + "/geckodriver")
url = "https://www.digitec.ch/de/s1/product/xiaomi-mi-9t-639-128gb-dual-sim-48mp-carbon-black-mobiltelefon-11245142"

# Opens the URL in a Firefox Browser Windows and loads the website
browser.get(url)
time.sleep(30)  # give enough time to load all scripts on website

# Extracts the specified part of the website -> here everything
# between the <head></head> tags
innerHTML = browser.execute_script("return document.head.innerHTML")

# Writes the innerHTML variable into a txt file
text_file = open("output.txt", "w")
text_file.write(innerHTML)
text_file.close

# Extracts the JSON Element which contains the price value
price_container = browser.execute_script(
    "return document.getElementById('json+ld').innerText"
)
low_price = json.loads(price_container)["offers"]["lowPrice"]
high_price = json.loads(price_container)["offers"]["highPrice"]

# Saves the price values with a time stamp in a CSV file
csv_file = open("prices.csv", "a")
time_stamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
csv_file.write(time_stamp + "," + str(low_price) + "," + str(high_price))
csv_file.write("\n")
csv_file.close

# Clean up (closer Browser) once task is completed
browser.close()

# Move the used webdriver back into the folder and rename it accordingly
if CURRENT_OS == "linux":
    shutil.move(
        CURRENT_DIRECTORY + "/geckodriver",
        CURRENT_DIRECTORY + "/webdrivers/geckodriver_linux64",
    )
else:
    shutil.move(
        CURRENT_DIRECTORY + "\geckodriver.exe",
        CURRENT_DIRECTORY + "\webdrivers\geckodriver_win64",
    )
