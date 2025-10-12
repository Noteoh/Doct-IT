import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QTextEdit, QMessageBox
)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UtopyaScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utopya Price Scraper")
        self.setGeometry(300, 200, 600, 500)

        layout = QVBoxLayout()

        # Brand selection
        self.brand_label = QLabel("Select Brand:")
        self.brand_combo = QComboBox()
        self.brand_combo.addItems(["Apple", "Samsung", "Huawei"])

        # Model selection
        self.model_label = QLabel("Select Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["iPhone 16e", "iPhone 15", "iPhone 14","A52"])

        # Button to scrape
        self.scrape_button = QPushButton("Get Prices")
        self.scrape_button.clicked.connect(self.scrape_data)

        # Text box for output
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        layout.addWidget(self.brand_label)
        layout.addWidget(self.brand_combo)
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_combo)
        layout.addWidget(self.scrape_button)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

    def scrape_data(self):
        brand = self.brand_combo.currentText()
        model = self.model_combo.currentText()

        self.output_box.clear()
        self.output_box.append(f"🔍 Searching for {brand} {model}...\n")

        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            driver_path = r"/Users/yassinetamant/PycharmProjects/PythonProject/chromedriver"
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Go to main site
            driver.get("https://www.utopya.fr")
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "span")))

            # Find the model link
            span = driver.find_element(
                By.XPATH,
                f"//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{model.lower()}')]"
            )
            url = span.find_element(By.XPATH, "..").get_attribute("href")
            self.output_box.append(f"🌐 Found URL: {url}\n")

            # Open model page
            driver.get(url)
            produits = WebDriverWait(driver, 15).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.product-item"))
            )

            self.output_box.append(f"📦 --- Products for {model} ---\n")

            for p in produits:
                try:
                    nom = p.find_element(By.CSS_SELECTOR, "a.product-item-link.name").text.strip()
                    prix = p.find_element(By.CSS_SELECTOR, "span.price").text.strip()
                    self.output_box.append(f"🧩 {nom}\n💶 {prix}\n")
                except Exception:
                    continue

            driver.quit()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred:\n{e}")
            self.output_box.append(f"\n❌ Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UtopyaScraperApp()
    window.show()
    sys.exit(app.exec_())
