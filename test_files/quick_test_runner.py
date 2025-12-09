#!/usr/bin/env python3
"""
QUICK START - Run this to test everything!

This script will:
1. Check if database is populated
2. Run quick tests (20 assertions)
3. Show summary

Usage: python quick_test_runner.py
"""

import mysql.connector
import sys

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "musicdb",
}


def check_database():
    """Check if database has data"""
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        cursor = mydb.cursor()
        cursor.execute("SELECT COUNT(*) FROM Songs")
        count = cursor.fetchone()[0]
        cursor.close()
        mydb.close()
        return count > 0
    except Exception as e:
        return False


def main():
    print("\n" + "=" * 60)
    print("QUICK TEST RUNNER - Music Database")
    print("=" * 60)

    # Check if database has data
    if not check_database():
        print("\n⚠️  Database appears to be empty!")
        print("\nPlease run test_music_db.py first to populate the database:")
        print("  python test_music_db.py")
        print("\nThen run this script again.")
        return False

    print("\n✓ Database has data, running quick tests...\n")

    # Run quick tests
    try:
        import subprocess
        import os
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_quick_path = os.path.join(script_dir, "test_quick.py")

        result = subprocess.run(
            [sys.executable, test_quick_path], capture_output=False, text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
