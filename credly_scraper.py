from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Ensure correct path to your WebDriver
service = Service("chromedriver.exe")  # Adjust if using EdgeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the Credly public profile
credly_url = "https://www.credly.com/users/bernadettesmail"
driver.get(credly_url)

# Wait for JavaScript to load content
time.sleep(5)  # Adjust if needed

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
            "Title": title,
            "Provider": provider,
            "Issue Date": issue_date,
            "Badge Image": badge_image
        })
    except Exception as e:
        print(f"Skipping one card due to error: {e}")

# Save extracted data to CSV
certificates_df = pd.DataFrame(certificates)
csv_filename = "Credly_Certificates.csv"
certificates_df.to_csv(csv_filename, index=False, encoding="utf-8")

print(f"✅ Extraction complete! Data saved as {csv_filename}")

# Close the browser
driver.quit()
