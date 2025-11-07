from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv

# --- Configuration du navigateur (connexion à Chrome lancé sur le port 9222)
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver_path = r"/Users/yassinetamant/PycharmProjects/PythonProject/chromedriver"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.utopya.fr")
time.sleep(5)  # on attend que la page et le menu se chargent

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

nav_div = soup.find("nav", class_="navigation")

with open("brands_models.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Model", "URL"])

    if nav_div:
        # 🔹 Niveau 1 : les marques (Apple, Samsung, Xiaomi, etc.)
        brands = nav_div.select("li.level1.category-item > a")

        for brand in brands:
            brand_name = brand.get_text(strip=True)
            brand_url = brand.get("href")

            if not brand_name or not brand_url:
                continue

            print(f"\n📱 Brand: {brand_name} → {brand_url}")

            # 🔹 Niveau 2 : les modèles (iPhone 15, Galaxy S23, etc.)
            submenu = brand.find_parent("li", class_="level1")
            if submenu:
                models = submenu.select("li.level2.category-item a")

                for model in models:
                    model_name = model.get_text(strip=True)
                    model_url = model.get("href")

                    if not model_name or not model_url:
                        continue

                    print(f"   └─ {model_name} → {model_url}")
                    writer.writerow([brand_name, model_name, model_url])
            else:
                writer.writerow([brand_name, "", brand_url])
    else:
        print("Navbar not found. Check class names.")

driver.quit()
print("Data saved in brands_models.csv")
