
import sqlite3

try:
    conn = sqlite3.connect('instance/phishing.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, email FROM target")
    rows = cursor.fetchall()
    print("Existing Targets:")
    for row in rows:
        print(row)
    conn.close()
except Exception as e:
    print(f"DB Error (might be empty or path wrong): {e}")
    # Try root path just in case
    try:
        conn = sqlite3.connect('phishing.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM target")
        rows = cursor.fetchall()
        print("Existing Targets (root):")
        for row in rows:
            print(row)
        conn.close()
    except Exception as e2:
        print(f"DB Error (root): {e2}")
