from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_draws_with_selenium(year):
    url = f"https://www.euro-millions.com/results-history-{year}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Lancer Chrome en arrière-plan
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Démarrer le navigateur Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print(f"🌐 Chargement de la page {url}...")
    driver.get(url)
    time.sleep(5)  # Attendre 5 secondes pour charger la page

    # Récupérer la page HTML
    html = driver.page_source
    driver.quit()

    # Utiliser BeautifulSoup pour extraire les données
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify()[:2000])  # Affiche les 2000 premiers caractères du HTML

    draws = soup.find_all("tr", class_="resultRow")

    if not draws:
        print(f"❌ Aucun tirage trouvé pour {year}. Vérifie la structure HTML.")
        return

    print(f"✅ {len(draws)} tirages récupérés pour {year} !")

    # Afficher les premiers résultats pour vérifier
    for draw in draws[:5]:  # Afficher les 5 premiers tirages
        print(draw.text.strip())

# Test avec l'année 2024
get_draws_with_selenium(2024)
