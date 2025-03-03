import requests
from bs4 import BeautifulSoup
import pandas as pd

def safe_decode(text):
    try:
        text = text.encode("latin1").decode("utf-8")
        text = text.replace("Â", "").replace("Ã", "").strip()
        return text
    except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
        return text if isinstance(text, str) else "Unknown"

def scrape_credly_certificates(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        certificates_data = []

        for cert in soup.find_all("div", class_="cr-standard-grid-item"):
            cert_name = cert.find("h3", class_="cr-standard-grid-item__title").text.strip() if cert.find("h3", class_="cr-standard-grid-item__title") else "Unknown"
            issuer = cert.find("div", class_="cr-standard-grid-item__organization").text.strip() if cert.find("div", class_="cr-standard-grid-item__organization") else "Unknown"
            issue_date = cert.find("span", class_="cr-standard-grid-item__issue-date").text.strip() if cert.find("span", class_="cr-standard-grid-item__issue-date") else "Unknown"
            cert_url = cert.find("a", class_="cr-standard-grid-item__cta")["href"] if cert.find("a", class_="cr-standard-grid-item__cta") else "No Link"
            
            certificates_data.append({
                "Certificate Name": safe_decode(cert_name),
                "Issuer": safe_decode(issuer),
                "Issue Date": safe_decode(issue_date),
                "Certificate URL": cert_url
            })

        df_certificates = pd.DataFrame(certificates_data)
        csv_filename = r"Credly_Certificates.csv"
        df_certificates.to_csv(csv_filename, index=False, encoding="utf-8")

        print(f"✅ Credly scraping complete! Data saved as: {csv_filename}")

    except requests.exceptions.RequestException as req_err:
        print(f"❌ Network error: {str(req_err)}")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    credly_url = "https://www.credly.com/users/bernadettesmail"
    scrape_credly_certificates(credly_url)
