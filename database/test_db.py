import sqlite3

conn = sqlite3.connect("database/gotham_service_desk.db")
cur = conn.cursor()

# Fetch all tickets
cur.execute("SELECT * FROM tickets")
for ticket in cur.fetchall():
    print(ticket)
    print("---------------------------")
    
conn.close()
