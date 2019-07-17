import requests
from selenium import webdriver
from lxml import html
import json
import time

browser = webdriver.Firefox()
url = "https://www.digitec.ch/de/s1/product/xiaomi-mi-9t-639-128gb-dual-sim-48mp-carbon-black-mobiltelefon-11245142"

browser.get(url)
time.sleep(30)
innerHTML = browser.execute_script("return document.head.innerHTML")

text_file = open("output.txt", "w")
text_file.write(innerHTML)
text_file.close

# print(innerHTML)

# result = requests.get(url)
# print(result)
# soup = BeautifulSoup(html_doc, "html.parser")

# price_container = soup.find("script", {"id": "json+ld"})
# print(price_container)
