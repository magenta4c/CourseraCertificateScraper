import subprocess
import sys

# Ensure required modules are installed
try:
    import selenium
    import pandas as pd
except ImportError:
    print("⚠ Installing missing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "pandas"])

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

service = Service("/usr/bin/chromedriver")  # Adjust if using GitHub-hosted runner
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Credly profile
credly_url = "https://www.credly.com/users/bernadettesmail"
driver.get(credly_url)

# Wait for JavaScript to load
time.sleep(5)

# Extract all badge cards
certificates = []
badge_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='mobile-badge-stackable-card']")

for card in badge_cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, ".skills-profile__edit-skills-profile__badge-card__badge-name__mobile").text
        issue_date = card.find_element(By.CSS_SELECTOR, ".skills-profile__edit-skills-profile__badge-card__issued-date__mobile").text.replace("Issued ", "")
        provider = card.find_element(By.CSS_SELECTOR, ".skills-profile__edit-skills-profile__badge-card__issuer-name__mobile").text
        badge_image = card.find_element(By.TAG_NAME, "img").get_attribute("src")

    certificates.append({
     "Course Name": course_name,
            "Provider": provider,
            "Date": issue_date,
            "Certificate Link": cert_link,
            "Provider Logo": badge_image,
            "Categories": categories
        })
    except Exception as e:
        print(f"Skipping one card due to error: {e}")

# Save to CSV
certificates_df = pd.DataFrame(certificates)
csv_filename = "Credly_Certificates.csv"
certificates_df.to_csv(csv_filename, index=False, encoding="utf-8")

print(f"✅ Extraction complete! Data saved as {csv_filename}")

# Close browser
driver.quit()
