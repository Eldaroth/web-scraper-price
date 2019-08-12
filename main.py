import json
import os
import shutil
import sys
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Constants to find out current Operating System and Working Directory
CURRENT_OS = sys.platform
CURRENT_DIRECTORY = os.getcwd()

def pre_checks_os(operating_system, current_directory):
    """ Checks for the OS and moves the according webdriver
    for Selenium to the current working directory"""
    if operating_system == "linux":
        if os.path.exists(os.path.join(current_directory, "geckodriver")) is False:
            shutil.move(
                os.path.join(current_directory, "webdrivers", "geckodriver_linux64"),
                os.path.join(current_directory, "geckodriver"),
            )
        time.sleep(5)
    # Same as above, just for a Windows System
    elif operating_system == "win32":
        if os.path.exists(os.path.join(current_directory, "geckodriver.exe")) is False:
            shutil.move(
                os.path.join(current_directory, "webdrivers", "geckodriver_win64.exe"),
                os.path.join(current_directory, "geckodriver.exe"),
            )
        time.sleep(5)
    # Checks whether CSV file already exists, otherwise creates one
    if os.path.exists(os.path.join(current_directory, "prices.csv")) is False:
        csv_file = open("prices.csv", "a")
        csv_file.write("Time;Device;Low Price;High Price\n")
        csv_file.close()
    # Checks whether url txt file already exists, otherwise gives warning
    if os.path.exists(os.path.join(current_directory, "url.txt")) is False:
        url_file = open("url.txt", "w")
        print("\nWARNING: No URL provided for program, please edit file 'url.txt' first!\n")
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
    # definition of executable_path only real necessary for Linux systems
)

# Opens the txt file containing all product urls and goes through them
url_file = open("url.txt", "r")
if os.stat(os.path.join(CURRENT_DIRECTORY, "url.txt")).st_size == 0:
    print("\nNo URL provided, please edit 'url.txt' file!\n")
    url_file.close()
    sys.exit()
for line in url_file:
    fetch_data(line)
    print("Fetching data for: \n" + line)

# Clean up (closer Browser) once task is completed
browser.close()
url_file.close()
print("\nSuccessfully finished!\n")

# Move the used webdriver back into the folder and rename it accordingly
if CURRENT_OS == "linux":
    shutil.move(
        os.path.join(CURRENT_DIRECTORY, "geckodriver"),
        os.path.join(CURRENT_DIRECTORY, "webdrivers", "geckodriver_linux64"),
    )
elif CURRENT_OS == "win32":
    shutil.move(
        os.path.join(CURRENT_DIRECTORY, "geckodriver.exe"),
        os.path.join(CURRENT_DIRECTORY, "webdrivers", "geckodriver_win64.exe"),
    )
