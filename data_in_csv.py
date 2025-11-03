from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv

# === Chrome setup ===
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver_path = r"/Users/yassinetamant/PycharmProjects/PythonProject/chromedriver"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# === Open website ===
driver.get("https://www.utopya.fr")
time.sleep(5)  # wait for page + navbar to load

# === Parse HTML with BeautifulSoup ===
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# === Find navbar ===
nav_div = soup.find("div", class_="nav-sections")  # adjust if needed

# === Open CSV file to store data ===
with open("brands_models.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Model", "URL"])

    if nav_div:
        # Find main brand items
        brands = nav_div.select("li.level1 > a")

        for brand in brands:
            brand_name = brand.get_text(strip=True)
            brand_url = brand.get("href")

            if not brand_name or not brand_url:
                continue

            print(f"\n📱 Brand: {brand_name} → {brand_url}")

            # Try to find submenu with models
            submenu = brand.find_next("ul", class_="submenu")

            if submenu:
                models = submenu.select("li.level2 > a")

                for model in models:
                    model_name = model.get_text(strip=True)
                    model_url = model.get("href")

                    if not model_name or not model_url:
                        continue

                    print(f"   └─ {model_name} → {model_url}")
                    writer.writerow([brand_name, model_name, model_url])

            else:
                # no models, write just brand
                writer.writerow([brand_name, "", brand_url])
    else:
        print("❌ Navbar not found. Check class names.")

driver.quit()
print("\n✅ Done! Data saved in brands_models.csv")
