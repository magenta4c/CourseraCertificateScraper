import subprocess
import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Ensure required modules are installed
try:
    import selenium
except ImportError:
    print("⚠ Installing missing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "pandas"])

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")  # Adjust for local execution
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Credly profile
credly_url = "https://www.credly.com/users/bernadettesmail"
driver.get(credly_url)
time.sleep(5)  # Wait for JavaScript to load

# **Scroll down to load all certificates**
scroll_pause_time = 2
screen_height = driver.execute_script("return window.innerHeight;")
scroll_attempts = 5

for i in range(scroll_attempts):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(scroll_pause_time)
    print(f"🔽 Scrolled down {i+1} times")

# Extract all badge cards
certificates = []
badge_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='mobile-badge-stackable-card']")
print(f"🔍 Found {len(badge_cards)} certificates")  # Debugging info

for card in badge_cards:
    try:
        course_name = card.find_element(By.CSS_SELECTOR, ".skills-profile__edit-skills-profile__badge-card__badge-name__mobile").text
        issue_date = card.find_element(By.CSS_SELECTOR, ".skills-profile__edit-skills-profile__badge-card__issued-date__mobile").text.replace("Issued ", "")
        provider = card.find_element(By.CSS_SELECTOR, ".skills-profile__edit-skills-profile__badge-card__issuer-name__mobile").text
        badge_image = card.find_element(By.TAG_NAME, "img").get_attribute("src")
        
        # Extract certificate link
        cert_link_element = card.find_element(By.CSS_SELECTOR, "a")
        cert_link = cert_link_element.get_attribute("href") if cert_link_element else "No Link"
        
        # Categories are not explicitly listed, using fallback
        categories = "General"

        certificates.append({
            "Course Name": course_name,
            "Provider": provider,
            "Date": issue_date,
            "Certificate Link": cert_link,
            "Provider Logo": badge_image,
            "Categories": categories
        })
        print(f"✅ Extracted: {course_name} from {provider}")

    except Exception as e:
        print(f"⚠ Skipping one card due to error: {e}")

# Save to CSV
certificates_df = pd.DataFrame(certificates)
csv_filename = "Credly_Certificates.csv"
certificates_df.to_csv(csv_filename, index=False, encoding="utf-8")

print(f"✅ Extraction complete! Data saved as {csv_filename}")

# Close browser
driver.quit()
