import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os

# 1. URL till sidan där FI listar alla kvartalsrapporter
BASE_URL = "https://www.fi.se"
LIST_URL = "https://www.fi.se/sv/vara-register/fondinnehav-per-kvartal/"

def download_latest_fi_funds():
    print(f"Letar efter senaste filen på {LIST_URL}...")
    
    # Hämta HTML-koden från sidan
    response = requests.get(LIST_URL)
    if response.status_code != 200:
        print("Kunde inte nå FI:s hemsida.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Hitta den första länken som slutar på .zip (vilket brukar vara det senaste kvartalet)
    latest_link = None
    for link in soup.find_all('a', href=True):
        if link['href'].endswith('.zip'):
            latest_link = link['href']
            break
            
    if not latest_link:
        print("Hittade ingen zip-fil.")
        return

    # Om länken är relativ, lägg till bas-URL:en
    if not latest_link.startswith("http"):
        latest_link = BASE_URL + latest_link

    print(f"Laddar ner: {latest_link}")

    # 2. Ladda ner ZIP-filen till minnet
    r = requests.get(latest_link)
    z = zipfile.ZipFile(io.BytesIO(r.content))

    # 3. Packa upp filerna i en mapp som heter 'fi_data'
    output_folder = "fi_data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    z.extractall(output_folder)
    print(f"Klart! {len(z.namelist())} XML-filer har sparats i mappen '{output_folder}'.")

if __name__ == "__main__":
    download_latest_fi_funds()