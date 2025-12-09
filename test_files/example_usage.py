"""
Example usage of the music database functions.
This file demonstrates how to use each function with simple examples.
"""

import os
import sys
import mysql.connector

# Ensure music_db.py (project root) is importable when running from test_files/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from music_db import *

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "music_database",
}


def example_usage():
    """Simple example demonstrating basic usage"""

    # Connect to database
    mydb = mysql.connector.connect(**DB_CONFIG)

    print("=== Example 1: Clear Database ===")
    clear_database(mydb)
    print("Database cleared!")

    print("\n=== Example 2: Load Single Songs ===")
    single_songs = [
        ("Blinding Lights", ("Pop", "Synth-pop"), "The Weeknd", "2019-11-29"),
        ("Shape of You", ("Pop",), "Ed Sheeran", "2017-01-06"),
        ("Bohemian Rhapsody", ("Rock", "Opera"), "Queen", "1975-10-31"),
    ]
    rejected = load_single_songs(mydb, single_songs)
    print(f"Loaded {len(single_songs)} songs, rejected: {rejected}")

    print("\n=== Example 3: Load an Album ===")
    albums = [
        (
            "25",
            "Pop",
            "Adele",
            "2015-11-20",
            ["Hello", "Send My Love", "When We Were Young"],
        ),
    ]
    rejected = load_albums(mydb, albums)
    print(f"Loaded {len(albums)} albums, rejected: {rejected}")

    print("\n=== Example 4: Load Users ===")
    users = ["alice", "bob", "charlie"]
    rejected = load_users(mydb, users)
    print(f"Loaded {len(users)} users, rejected: {rejected}")

    print("\n=== Example 5: Load Ratings ===")
    ratings = [
        ("alice", ("The Weeknd", "Blinding Lights"), 5, "2020-01-15"),
        ("bob", ("Queen", "Bohemian Rhapsody"), 5, "2020-01-20"),
        ("charlie", ("Ed Sheeran", "Shape of You"), 4, "2020-01-25"),
    ]
    rejected = load_song_ratings(mydb, ratings)
    print(f"Loaded {len(ratings)} ratings, rejected: {rejected}")

    print("\n=== Example 6: Get Top Genres ===")
    top_genres = get_top_song_genres(mydb, 3)
    print("Top 3 genres:")
    for genre, count in top_genres:
        print(f"  {genre}: {count} songs")

    print("\n=== Example 7: Get Artists with Albums and Singles ===")
    artists = get_album_and_single_artists(mydb)
    print(f"Artists with both albums and singles: {artists}")

    print("\n=== Example 8: Get Most Prolific Artists ===")
    prolific = get_most_prolific_individual_artists(mydb, 3, (2015, 2020))
    print("Top 3 most prolific artists (2015-2020):")
    for artist, count in prolific:
        print(f"  {artist}: {count} singles")

    print("\n=== Example 9: Get Most Rated Songs ===")
    most_rated = get_most_rated_songs(mydb, (2020, 2020), 5)
    print("Top 5 most rated songs in 2020:")
    for song, artist, count in most_rated:
        print(f"  {song} by {artist}: {count} ratings")

    print("\n=== Example 10: Get Most Engaged Users ===")
    engaged = get_most_engaged_users(mydb, (2020, 2020), 3)
    print("Top 3 most engaged users in 2020:")
    for user, count in engaged:
        print(f"  {user}: {count} songs rated")

    # Close connection
    mydb.close()
    print("\n✓ All examples completed!")


if __name__ == "__main__":
    print("Make sure to update DB_CONFIG before running!")
    print("Press Enter to continue...")
    input()
    example_usage()
