import sqlite3

def match_worker(job_skill, job_availability, job_location="unknown"):
    conn = sqlite3.connect("job_platform.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, skill, availability, location 
        FROM workers 
        WHERE skill = ? AND availability = ? AND location = ?
    """, (job_skill, job_availability, job_location))
    match = cursor.fetchone()
    conn.close()
    return match