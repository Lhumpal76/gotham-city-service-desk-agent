"""
setup_db.py

This script sets up the Gotham Service Desk database using SQLite.

It performs the following steps:
1. Connects to (or creates) the SQLite database file 'gotham_service_desk.db'.
2. Creates a 'tickets' table if it does not already exist. Each ticket has:
   - id: Auto-incrementing primary key
   - title: Short description of the crime/event
   - assigned_to: The Gotham resident assigned to handle it
   - status: Current status of the ticket ('open', 'in progress', 'closed')
   - priority: Priority level of the ticket ('low', 'medium', 'high')
3. Seeds the table with initial sample tickets involving Gotham City characters.
4. Commits changes and closes the database connection.

After running, the database will be ready for queries or integration with
future agent tools.
"""

import sqlite3
import os
import random  # for shuffling

# Ensure the database folder exists
os.makedirs("database", exist_ok=True)

# Connect to the database file
conn = sqlite3.connect("database/gotham_service_desk.db")
cur = conn.cursor()

# Create tickets table with 'resolution' column
cur.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    resolution TEXT
)
""")

# Seed 25 tickets
tickets = []

# 10 closed Batman tickets with detailed resolutions
batman_resolutions = [
    "Investigated the crime scene, gathered fingerprints and security footage, then set a trap using a decoy to lure the intruder into custody.",
    "Analyzed break-in patterns and used night-vision drones to track movement, cornering the intruder on the rooftop and apprehending him without collateral damage.",
    "Disguised himself and infiltrated the suspect's hideout, using stealth tactics to disable traps and capture the intruder safely.",
    "Examined surveillance data and predicted the intruder’s next target, intercepting him mid-action and recovering stolen goods.",
    "Set up a controlled bait scenario in the tower lobby, monitored remotely, and captured the intruder using non-lethal gadgets.",
    "Used forensic evidence to deduce the intruder’s identity, followed him through Gotham’s alleyways, and incapacitated him with precise timing and agility.",
    "Coordinated with Commissioner Gordon to track stolen property, then ambushed the intruder while ensuring civilians remained safe.",
    "Installed tracking devices on the intruder’s known accomplices, anticipated their movements, and captured the main suspect using grappling and stealth tactics.",
    "Mapped out all entry points and escape routes in Wayne Tower, set surveillance traps, and apprehended the intruder without raising alarms.",
    "Monitored financial and digital records to locate the intruder, then executed a tactical interception on the roof, retrieving stolen items safely."
]

for i, resolution in enumerate(batman_resolutions, start=1):
    tickets.append((
        f"Break-in at Wayne Tower #{i}",
        "Batman",
        "closed",
        "high",
        resolution
    ))

# 1 open Batman ticket with the same subject matter
tickets.append((
    "Break-in at Wayne Tower #11",
    "Batman",
    "open",
    "high",
    None
))

# Other tickets (14 remaining)
other_tickets = [
    ("Joker causing chaos downtown", "Commissioner Gordon", "in progress", "high", None),
    ("Cat burglar in museum", "Catwoman", "open", "medium", None),
    ("Poison Ivy spreading plants in park", "Batman", "open", "medium", None),
    ("Penguin smuggling rare birds", "Commissioner Gordon", "closed", "low", "Tracked Penguin to the docks, intercepted his shipment, and returned the birds safely to the sanctuary."),
    ("Riddler's cryptic puzzle in city hall", "Batman", "in progress", "high", None),
    ("Arson at Gotham Docks", "Commissioner Gordon", "closed", "high", "Led firefighters to contain the blaze, examined evidence, and arrested the arsonist for prosecution."),
    ("Smuggling operation in East End", "Batman", "closed", "medium", "Disguised as a buyer, followed the smugglers to their warehouse, and coordinated a midnight raid to secure the contraband."),
    ("Bank heist foiled at Gotham Bank", "Batman", "closed", "high", "Analyzed the heist plans, predicted the timing, and disabled the robbers’ getaway using advanced surveillance and grappling hooks."),
    ("Poison gas in subway", "Batman", "closed", "high", "Detected the gas canisters using sensors, evacuated civilians, and neutralized the toxins using his portable filtration units."),
    ("Street racing causing accidents", "Commissioner Gordon", "open", "medium", None),
    ("Mugging spree in Narrows", "Batman", "closed", "medium", "Tracked patterns of the muggings, used disguise to catch suspects in the act, and returned stolen goods."),
    ("Hack into Wayne Enterprises servers", "Batman", "closed", "high", "Traced the hacker’s IP, infiltrated their network, and secured sensitive company data without alerting the perpetrator."),
    ("Hostage situation at Gotham Mall", "Commissioner Gordon", "in progress", "high", None),
    ("False alarms in Gotham Police HQ", "Commissioner Gordon", "closed", "low", "Investigated alarm triggers, recalibrated the system, and confirmed there was no threat.")
]

tickets.extend(other_tickets)

# Shuffle tickets before inserting
random.shuffle(tickets)

# Insert into database
cur.executemany(
    "INSERT INTO tickets (title, assigned_to, status, priority, resolution) VALUES (?, ?, ?, ?, ?)",
    tickets
)

# Commit and close
conn.commit()
conn.close()

print("Gotham service desk database created and seeded with 25 shuffled tickets successfully!")
