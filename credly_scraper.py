from bs4 import BeautifulSoup
import pandas as pd

# Load the saved Credly HTML file
html_file = "saved_resource.html"
with open(html_file, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract all badge cards
badge_cards = soup.find_all("div", {"data-testid": "mobile-badge-stackable-card"})

# List to store extracted data
certificates = []

for card in badge_cards:
    # Extract certificate title
    title_tag = card.find("span", class_="skills-profile__edit-skills-profile__badge-card__badge-name__mobile")
    title = title_tag.text.strip() if title_tag else "Unknown Title"

    # Extract issue date
    date_tag = card.find("div", class_="skills-profile__edit-skills-profile__badge-card__issued-date__mobile")
    issue_date = date_tag.text.replace("Issued ", "").strip() if date_tag else "Unknown Date"

    # Extract provider name
    provider_tag = card.find("div", class_="skills-profile__edit-skills-profile__badge-card__issuer-name__mobile")
    provider = provider_tag.text.strip() if provider_tag else "Unknown Provider"

    # Extract badge image
    img_tag = card.find("img")
    badge_image = img_tag["src"] if img_tag else "No Image"

    # Store the extracted data
    certificates.append({
        "Title": title,
        "Provider": provider,
        "Issue Date": issue_date,
        "Badge Image": badge_image
    })

# Convert to a DataFrame and save as CSV
certificates_df = pd.DataFrame(certificates)
certificates_df.to_csv("Credly_Certificates.csv", index=False, encoding="utf-8")

print("✅ Extraction complete! Data saved as Credly_Certificates.csv")
