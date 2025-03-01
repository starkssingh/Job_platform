import sqlite3

def init_db():
    conn = sqlite3.connect("job_platform.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            skill TEXT,
            availability TEXT,
            location TEXT
        )
    """)
    conn.commit()
    conn.close()

def store_worker_profile(name, skill, availability, location="unknown"):
    conn = sqlite3.connect("job_platform.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workers (name, skill, availability, location) VALUES (?, ?, ?, ?)",
                   (name, skill, availability, location))
    conn.commit()
    conn.close()