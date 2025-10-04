from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver_path = r"/Users/yassinetamant/PycharmProjects/PythonProject/chromedriver"
service = Service(driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.utopya.fr/apple/iphone/iphone-16e.html")
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

produits = soup.find_all("div", class_="product-item")


for p in produits:
    nom = p.find("a", class_="product-item-link name")
    prix = p.find("span", class_="price")

    if nom and prix:  # éviter erreurs si pas trouvé
        print("Nom :", nom.get_text(strip=True))
        print("Prix :", prix.get_text(strip=True))