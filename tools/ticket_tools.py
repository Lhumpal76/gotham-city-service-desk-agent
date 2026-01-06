"""
Connects to your SQLite database
Queries for closed tickets
Returns structured data the agent can work with
- Can only read from the database
"""
import sqlite3
from typing import List, Dict, Any

def lookup_closed_tickets() -> List[Dict[str, Any]]:
    """
    Queries the database for all closed tickets.

    Returns:
        List of ticket dictionaries with all ticket information
    """
    # Connect to the database
    conn = sqlite3.connect('database/gotham_service_desk.db')
    cursor = conn.cursor()

    # Query closed tickets
    cursor.execute('''
        SELECT id, title, assigned_to, status, priority, resolution
        FROM tickets
        WHERE status = 'closed'
    ''')

    # Fetch results
    tickets = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    # Close database connection
    conn.close()

    # Convert to list of dictionaries
    ticket_dicts = []
    for ticket in tickets:
        ticket_dict = {column_names[i]: ticket[i] for i in range(len(column_names))}
        ticket_dicts.append(ticket_dict)

    return ticket_dicts