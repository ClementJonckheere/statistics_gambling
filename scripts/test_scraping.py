import os
from dotenv import load_dotenv
from api.external import get_draws_by_year

# Charger les variables d'environnement
load_dotenv()

# Tester avec l'année actuelle
draws = get_draws_by_year(2025)

# Vérifier le résultat
if draws:
    print(f"✅ {len(draws)} tirages récupérés avec succès pour 2025 !")
else:
    print("❌ Aucun tirage trouvé. Vérifie le scraping.")
