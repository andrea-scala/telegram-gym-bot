import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "gymbot.db")

def salva_scheda(user_id, testo):
    giorni = {}
    lines = [l.strip() for l in testo.strip().splitlines() if l.strip()]
    giorno_idx = 1
    current_giorno = f"Giorno {giorno_idx}"
    giorni[current_giorno] = []

    for line in lines:
        if any(char.isdigit() for char in line):
            parts = line.split()
            serie_rip = next((p for p in parts if "x" in p), "")
            note = line.replace(serie_rip, "").replace(parts[0], "", 1).strip() if serie_rip else ""
            giorni[current_giorno].append({
                "titolo": parts[0].capitalize(),
                "serie_ripetizioni": serie_rip,
                "note": note
            })
        else:
            giorno_idx += 1
            current_giorno = f"Giorno {giorno_idx}"
            giorni[current_giorno] = []

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS schede (user_id INTEGER PRIMARY KEY, testo TEXT)")
        c.execute("INSERT OR REPLACE INTO schede (user_id, testo) VALUES (?, ?)", (user_id, json.dumps(giorni)))
        conn.commit()

def carica_scheda(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT testo FROM schede WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        return json.loads(row[0]) if row else None

def salva_sessione(user_id, data, giorno, allenamento):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS sessioni (
            user_id INTEGER,
            data TEXT,
            giorno TEXT,
            esercizio TEXT,
            serie_index INTEGER,
            ripetizioni INTEGER,
            carico REAL
        )""")
        for esercizio in allenamento:
            titolo = esercizio["esercizio"]
            for i, serie in enumerate(esercizio["serie"]):
                c.execute("""
                INSERT INTO sessioni (user_id, data, giorno, esercizio, serie_index, ripetizioni, carico)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, data, giorno, titolo, i+1, serie["ripetizioni"], serie["carico"]))
        conn.commit()

def carica_storico(user_id, esercizio_parziale):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
        SELECT data, serie_index, ripetizioni, carico
        FROM sessioni
        WHERE user_id = ? AND LOWER(esercizio) LIKE ?
        ORDER BY data, serie_index
        """, (user_id, f"%{esercizio_parziale.lower()}%"))
        return c.fetchall()
