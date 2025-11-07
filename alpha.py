import csv
import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

# Charger CSV
def load_data():
    data = []
    with open("brands_models.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

data = load_data()
brands = sorted(set(row["Brand"] for row in data if row["Brand"]))
models_by_brand = {}
for row in data:
    brand = row["Brand"]
    model = row["Model"]
    if brand not in models_by_brand:
        models_by_brand[brand] = []
    if model and model not in models_by_brand[brand]:
        models_by_brand[brand].append(model)

# Interface
root = tk.Tk()
root.title("Test Scrap")
root.geometry("400x300")

tk.Label(root, text="Choisir une marque :").pack(pady=5)
brand_var = tk.StringVar()
brand_menu = ttk.Combobox(root, textvariable=brand_var, values=brands, state="readonly")
brand_menu.pack()

tk.Label(root, text="Choisir un modèle :").pack(pady=5)
model_var = tk.StringVar()
model_menu = ttk.Combobox(root, textvariable=model_var, state="readonly")
model_menu.pack()

def update_models(event):
    brand = brand_var.get()
    models = models_by_brand.get(brand, [])
    model_menu["values"] = models
    model_menu.set("")

brand_menu.bind("<<ComboboxSelected>>", update_models)

def show_parts():
    brand = brand_var.get()
    model = model_var.get()

    url = None
    for row in data:
        if row["Brand"] == brand and row["Model"] == model:
            url = row["URL"]
            break

    if not url:
        messagebox.showwarning("Erreur", "Aucun lien trouvé pour ce modèle.")
        return

    # --- Scraper les produits ---
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver_path = r"/Users/yassinetamant/PycharmProjects/PythonProject/chromedriver"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    produits = soup.find_all("div", class_="product-item")

    result_text = ""
    for p in produits:
        nom = p.find("a", class_="product-item-link name")
        prix = p.find("span", class_="price")
        if nom and prix:
            result_text += f"{nom.get_text(strip=True)} - {prix.get_text(strip=True)}\n"

    driver.quit()

    if result_text:
        messagebox.showinfo("Pièces disponibles", result_text)
    else:
        messagebox.showinfo("Résultat", "Aucune pièce trouvée pour ce modèle.")

tk.Button(root, text="Voir les pièces", command=show_parts).pack(pady=20)

root.mainloop()
