import os
from psycopg import conninfo, connect, Error, Connection, rows

class Database():
    def __init__(self):
        try:
            if hasattr(self, 'conn') and self.conn != None:
                self.close()

            db_url = os.getenv("DATABASE_URL")
            schema = os.getenv("DB_SCHEMA")

            db_info = conninfo.conninfo_to_dict(db_url, options="-c search_path="+schema)

            self.conn = connect(**db_info, row_factory=rows.dict_row)
            self.cur = self.conn.cursor()
        except Error as error:
            print ("Error while connecting to db:", error)

    def getCursor(self):
        return self.cur

    def getConn(self) -> Connection:
        return self.conn

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

        # ✅ Récupérer les statistiques des numéros et étoiles

    def get_statistics(self):
        self.cur.execute("SELECT number, frequency, type FROM draw_statistics ORDER BY frequency DESC;")
        return self.cur.fetchall()

        # ✅ Récupérer les numéros prédits

    def get_predictions(self):
        self.cur.execute("SELECT number FROM draw_statistics WHERE type='number' ORDER BY frequency DESC LIMIT 5;")
        predicted_numbers = [row["number"] for row in self.cur.fetchall()]

        self.cur.execute("SELECT number FROM draw_statistics WHERE type='star' ORDER BY frequency DESC LIMIT 2;")
        predicted_stars = [row["number"] for row in self.cur.fetchall()]

        return {"numbers": predicted_numbers, "stars": predicted_stars}

        # ✅ Mettre à jour les statistiques

    def update_statistics(self, num_counter, star_counter):
        self.cur.execute("DELETE FROM draw_statistics;")  # Vider la table avant d'ajouter les nouvelles stats

        for num, count in num_counter.items():
            self.cur.execute("INSERT INTO draw_statistics (number, frequency, type) VALUES (%s, %s, 'number');",
                             (num, count))

        for star, count in star_counter.items():
            self.cur.execute("INSERT INTO draw_statistics (number, frequency, type) VALUES (%s, %s, 'star');",
                             (star, count))

        self.commit()