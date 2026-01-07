import sys
import os

# Import the database setup and FAISS setup modules
from setup_db import main as setup_db
from setup_faiss import main as setup_faiss
from test_faiss import main as test_faiss

def main():
    """
    Run the entire pipeline: database setup -> FAISS index creation -> test
    """
    print("=" * 50)
    print("Gotham City Service Desk Setup")
    print("=" * 50)

    print("\nStep 1: Setting up the SQLite database...")
    # Run the database setup
    setup_db()

    print("\nStep 2: Creating the FAISS index...")
    # Run the FAISS setup
    setup_faiss()

    print("\nStep 3: Testing the FAISS index...")
    # Run the FAISS test
    test_faiss()

    print("\n" + "=" * 50)
    print("Setup Complete! The system is ready to use.")
    print("=" * 50)

if __name__ == "__main__":
    main()