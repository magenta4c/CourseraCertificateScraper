import requests
import pandas as pd
from bs4 import BeautifulSoup

print(pd.__version__)  # This should output the installed pandas version

def safe_decode(text):
    """Safely decode text to handle encoding issues."""
    try:
        text = text.encode("latin1").decode("utf-8")
        text = text.replace("Â", "").replace("Ã", "").strip()  # Remove encoding artifacts
        return text
    except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
        return text if isinstance(text, str) else "Unknown"

try:
    # Load the HTML file from the URL
    url = "https://www.coursera.org/learner/magenta4c"  # Replace with the actual profile URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Initialize a list to store extracted certificate data
    certificates_data = []

    # Searching for certificate sections (list items in the course list)
    for cert_section in soup.find_all("div", role="listitem"):
        # Extracting course name
        course_name_tag = cert_section.find("h3", class_="css-6ecy9b")
        course_name = safe_decode(course_name_tag.text.strip()) if course_name_tag else None
        
        if not course_name:
            continue  # Skip entries with missing course names

        # Extracting provider name
        provider_tag = cert_section.find("p", class_="css-vac8rf")
        provider_text = provider_tag.find("span").text if provider_tag and provider_tag.find("span") else "Unknown Provider"
        provider = safe_decode(provider_text.split("·")[0].strip())  # Ensure correct provider extraction

        # Extracting provider logo URL
        logo_tag = cert_section.find("img", src=True)
        provider_logo = logo_tag["src"] if logo_tag else "No Logo"

        # Extracting certificate verification link
        cert_link_tag = cert_section.find("a", class_="cds-119", href=True)
        cert_link = cert_link_tag["href"] if cert_link_tag else "No Link"

        # Extracting completion date
        date_tag = cert_section.find("p", class_="css-vac8rf", string=lambda text: text and "Completed" in text)
        date = safe_decode(date_tag.find("span").text.replace("Completed", "").strip()) if date_tag and date_tag.find("span") else "Unknown Date"

        # Extracting category tags
        category_tags = cert_section.find_all("span", class_="css-o5tswl")
        categories = ", ".join([safe_decode(tag.get_text(strip=True)) for tag in category_tags]) if category_tags else "General"

        # Append the extracted data to the list
        certificates_data.append({
            "Course Name": course_name,
            "Provider": provider,
            "Date": date,
            "Certificate Link": cert_link,
            "Provider Logo": provider_logo,
            "Categories": categories
        })

    # Convert the extracted data to a DataFrame
    df_certificates = pd.DataFrame(certificates_data)

    # Fixing missing provider logos by assigning the most common logo per provider
    provider_logo_map = df_certificates.groupby("Provider")["Provider Logo"].apply(lambda x: x.value_counts().idxmax()).to_dict()

    # Updating missing provider logos with correct values
    for i in range(len(df_certificates)):
        if not df_certificates.at[i, "Provider Logo"].startswith("http"):
            provider = df_certificates.at[i, "Provider"]
            df_certificates.at[i, "Provider Logo"] = provider_logo_map.get(provider, "No Logo Available")

    # Save to CSV file with UTF-8 encoding
    csv_filename = r"I:\My Drive\IBM ai product manager\Code\Coursera_Certificates.csv"
    df_certificates.to_csv(csv_filename, index=False, encoding="utf-8")

    print(f"✅ Extraction complete! Data saved as: {csv_filename}")

except requests.exceptions.RequestException as req_err:
    print(f"❌ Network error: {str(req_err)}")
except Exception as e:
    print(f"❌ An error occurred: {str(e)}")
