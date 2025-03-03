import pandas as pd

# Load CSV file containing badge URLs
csv_file = "Credly_Certificates.csv"
df = pd.read_csv(csv_file, header=None, names=["Badge_URL"])

# Function to extract badge ID from URL
def extract_badge_id(url):
    return url.strip().split("/")[-1]  # Extracts the last part of the URL

# Generate embed codes
embed_codes = []
for url in df["Badge_URL"]:
    badge_id = extract_badge_id(url)
    embed_code = f'<div data-iframe-width="400" data-iframe-height="270" data-share-badge-id="{badge_id}" data-share-badge-host="https://www.credly.com"></div><script type="text/javascript" async src="//cdn.credly.com/assets/utilities/embed.js"></script>'
    embed_codes.append({"Badge_ID": badge_id, "Embed_Code": embed_code})

# Convert to DataFrame and save as CSV
embed_df = pd.DataFrame(embed_codes)
embed_df.to_csv("Credly_Embeds.csv", index=False, encoding="utf-8")

# Print output
print("✅ Embed codes generated! Saved as Credly_Embeds.csv.")
