from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Setup Chrome options for headless mode (needed for GitHub Actions)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Credly page
url = "https://www.credly.com/users/bernadettesmail"
driver.get(url)

# Wait for page to load
time.sleep(5)

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract badge IDs
badge_cards = soup.find_all("div", {"data-share-badge-id": True})

badge_ids = []
for card in badge_cards:
    badge_id = card["data-share-badge-id"]
    badge_ids.append({"Badge ID": badge_id})

# Convert to DataFrame and save as CSV
df = pd.DataFrame(badge_ids)
df.to_csv("Credly_Badge_IDs.csv", index=False, encoding="utf-8")

# Generate Embed Code
embed_code_list = [
    f'<div data-iframe-width="400" data-iframe-height="270" data-share-badge-id="{badge["Badge ID"]}" data-share-badge-host="https://www.credly.com"></div>'
    '<script type="text/javascript" async src="//cdn.credly.com/assets/utilities/embed.js"></script>'
    for badge in badge_ids
]

# Save Embed Code to a File
with open("Credly_Embeds.html", "w", encoding="utf-8") as file:
    file.write("\n".join(embed_code_list))

print("✅ Extraction complete! Data saved as Credly_Badge_IDs.csv and Credly_Embeds.html")

# Close WebDriver
driver.quit()
