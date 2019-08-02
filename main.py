from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import sys
import shutil
import os
import json

# Constants to find out current Operating System and Working Directory
CURRENT_OS = sys.platform
CURRENT_DIRECTORY = os.getcwd()

def pre_checks_os(operating_system, current_directory):
    # Checks if OS is a Linux System and moves the according webdriver
    # for Selenium to the current working directory
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
            csv_file.write("Time;Device;Low Price;High Price\n")
            csv_file.close()
        time.sleep(5)
        # Checks whether url txt file already exists, otherwise gives warning
        if os.path.exists(current_directory + "/url.txt") is False:
            url_file = open("url.txt", "w")
            print("WARNING: No URL provided for program, please edit file 'url.txt' first")
            url_file.close()
            sys.exit()

    # Same as above, just for a Windows System
    elif operating_system == "win32":
        if os.path.exists(current_directory + r"\geckodriver.exe") is False:
            shutil.move(
                current_directory + r"\webdrivers\geckodriver_win64.exe",
                current_directory + r"\geckodriver.exe",
            )
        time.sleep(5)
        # Checks whether CSV file already exists, otherwise creates one
        if os.path.exists(current_directory + r"\prices.csv") is False:
            csv_file = open("prices.csv", "a")
            csv_file.write("Time;Device;Low Price;High Price\n")
            csv_file.close()
        time.sleep(5)
        # Checks whether url txt file already exists, otherwise gives warning
        if os.path.exists(current_directory + r"\url.txt") is False:
            url_file = open("url.txt", "w")
            print("WARNING: No URL provided for program, please edit file 'url.txt' first")
            url_file.close()
            sys.exit()

def fetch_data(url):
    # Opens the URL in a Firefox Browser Windows and loads the website
    browser.get(url)
    # Extracts the JSON Element which contains the price value
    price_container = browser.execute_script(
        "return document.getElementById('json+ld').innerText"
    )
    low_price = json.loads(price_container)["offers"]["lowPrice"]
    high_price = json.loads(price_container)["offers"]["highPrice"]
    device = json.loads(price_container)["name"]
    # Saves the price values with a time stamp in a CSV file
    csv_file = open("prices.csv", "a")
    time_stamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    csv_file.write(time_stamp + ";" + device + ";" + str(low_price) + ";" + str(high_price))
    csv_file.write("\n")
    csv_file.close()


pre_checks_os(CURRENT_OS, CURRENT_DIRECTORY)

# Defines which browser will be used to open website with Selenium
options = Options()
options.headless = True
browser = webdriver.Firefox(
    options=options, executable_path=CURRENT_DIRECTORY + "/geckodriver"
)

# Opens the txt file containing all product urls and goes through them
url_file = open("url.txt", "r")
for line in url_file:
    fetch_data(line)
    print(line)

# Clean up (closer Browser) once task is completed
browser.close()

# Move the used webdriver back into the folder and rename it accordingly
if CURRENT_OS == "linux":
    shutil.move(
        CURRENT_DIRECTORY + "/geckodriver",
        CURRENT_DIRECTORY + "/webdrivers/geckodriver_linux64",
    )
elif CURRENT_OS == "win32":
    shutil.move(
        CURRENT_DIRECTORY + r"\geckodriver.exe",
        CURRENT_DIRECTORY + r"\webdrivers\geckodriver_win64.exe",
    )
