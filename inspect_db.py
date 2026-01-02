import sqlite3
import pandas as pd

# 1. Conectare
conn = sqlite3.connect('affective_data.db')

# 2. Citim ultimele 10 înregistrări
print("--- ULTIMELE 10 MĂSURĂTORI ---")
df = pd.read_sql_query("SELECT * FROM Measurements ORDER BY id DESC LIMIT 10", conn)
print(df)

# 3. Statistici rapide (ca să vezi dacă varianta "Redness" chiar variază)
print("\n--- STATISTICI (Min/Max/Medie) ---")
stats = pd.read_sql_query("SELECT AVG(cheek_redness), MIN(cheek_redness), MAX(cheek_redness) FROM Measurements", conn)
print(stats)

conn.close()
