import psycopg
from collections import Counter
from dotenv import load_dotenv
from api.utils.db import Database

def analyze_and_update_statistics():
    db = Database()

    # Récupérer tous les tirages
    cursor = db.getCursor()
    cursor.execute("SELECT numbers, stars FROM draws;")
    results = cursor.fetchall()

    # Initialiser les compteurs
    num_counter = Counter()
    star_counter = Counter()

    # Traiter les résultats
    for row in results:
        num_counter.update(row["numbers"])  # Compter les numéros
        star_counter.update(row["stars"])   # Compter les étoiles

    # Insérer ou mettre à jour les statistiques
    update_statistics(db, num_counter, 'number')
    update_statistics(db, star_counter, 'star')

    print("✅ Statistiques mises à jour dans PostgreSQL !")
    db.close()

def update_statistics(db, counter, stat_type):
    """
    Met à jour la table `draw_statistics` avec les fréquences calculées.
    """
    for number, frequency in counter.items():
        query = """
        INSERT INTO draw_statistics (number, frequency, type)
        VALUES (%s, %s, %s)
        ON CONFLICT (number, type)
        DO UPDATE SET frequency = EXCLUDED.frequency;
        """
        db.getCursor().execute(query, (number, frequency, stat_type))

    db.commit()

if __name__ == "__main__":
    analyze_and_update_statistics()
