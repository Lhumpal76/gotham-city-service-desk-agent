import sqlite3
import json

# Open and read the JSON file
with open("database/tickets.json", "r") as file:
    data = json.load(file)

# Create database and connect
conn = sqlite3.connect('database/gotham_service_desk.db')
cursor = conn.cursor()

# Create tickets table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    assigned_to TEXT,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    resolution TEXT
)
''')

# Insert tickets from JSON file
for ticket in data['tickets']:
    cursor.execute('''
        INSERT OR REPLACE INTO tickets (id, title, assigned_to, status, priority, resolution)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        ticket['id'],
        ticket['title'],
        ticket['assigned_to'],
        ticket['status'],
        ticket['priority'],
        ticket.get('resolution')  # Use .get() to handle None values
    ))

# Commit changes
conn.commit()

# Verify the data
cursor.execute('SELECT COUNT(*) FROM tickets')
print(f"Total tickets inserted: {cursor.fetchone()[0]}")

conn.close()
print("\nDatabase created successfully: database/gotham_service_desk.db")