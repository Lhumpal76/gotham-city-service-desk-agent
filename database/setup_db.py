import sqlite3
import json
import os

def main():
    """
    Create and populate the SQLite database from tickets.json.
    Old database file is deleted if it exists.
    """
    db_path = 'database/gotham_service_desk.db'

    # Remove old database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Old database removed: {db_path}")

    # Open and read the JSON file
    with open("database/tickets.json", "r") as file:
        data = json.load(file)

    # Create database and connect
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tickets table
    cursor.execute('''
    CREATE TABLE tickets (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        assigned_to TEXT,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        resolution TEXT,
        description TEXT
    )
    ''')

    # Insert tickets from JSON file
    for ticket in data['tickets']:
        cursor.execute('''
            INSERT INTO tickets (id, title, assigned_to, status, priority, resolution, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            ticket['id'],
            ticket['title'],
            ticket['assigned_to'],
            ticket['status'],
            ticket['priority'],
            ticket.get('resolution'),
            ticket.get('description')
        ))

    # Commit changes
    conn.commit()

    # Verify the data
    cursor.execute('SELECT COUNT(*) FROM tickets')
    print(f"Total tickets inserted: {cursor.fetchone()[0]}")

    conn.close()
    print(f"\nDatabase created successfully: {db_path}")

if __name__ == "__main__":
    main()
