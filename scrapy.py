from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver_path = "/Users/yassinetamant/PycharmProjects/PythonProject/chromedriver"
service = Service(driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.utopya.fr/apple/iphone/iphone-15.html")
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
price_tag = soup.find("span", class_="price")

if price_tag:
    print("Prix trouvé (via BeautifulSoup) :", price_tag.text.strip())
else:
    print("Aucun prix trouvé dans le HTML extrait.")

