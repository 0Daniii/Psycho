
import sqlite3
import pandas as pd
import os

# 1. Găsim calea corectă
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "affective_data.db")

print(f"🔍 Caut baza de date la: {db_path}")

# 2. Verificăm dacă fișierul există
if not os.path.exists(db_path):
    print(f"❌ NU există fișierul! Rulează întâi main.py.")
    exit()

# 3. Citim datele
conn = sqlite3.connect(db_path)
try:
    # Vedem câte rânduri sunt în total
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Measurements")
    total_rows = cursor.fetchone()[0]
    
    print(f"✅ Total înregistrări găsite: {total_rows}")

    if total_rows > 0:
        print("\n--- ULTIMELE 10 MĂSURĂTORI REALE ---")
        # Citim ultimele 10 rânduri
        df = pd.read_sql_query("SELECT * FROM Measurements ORDER BY id DESC LIMIT 10", conn)
        print(df)
    else:
        print("⚠️ Baza de date există, dar este GOALĂ. (Nu s-a detectat fața?)")
except Exception as e:
    print(f"Eroare la citire: {e}")
finally:
    conn.close()
