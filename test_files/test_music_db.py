import os
import sys
import mysql.connector

# Ensure music_db.py (project root) is importable when running from test_files/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from music_db import *

# Database configuration - UPDATE THESE VALUES
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",  # Change this to your MySQL password
    "database": "musicdb",  # Change this to your database name
}


def connect_db():
    """Connect to the MySQL database"""
    return mysql.connector.connect(**DB_CONFIG)


def test_clear_database():
    """Test clearing the database"""
    print("\n=== Testing clear_database ===")
    mydb = connect_db()
    clear_database(mydb)
    print("✓ Database cleared successfully")
    mydb.close()


def test_load_single_songs():
    """Test loading single songs"""
    print("\n=== Testing load_single_songs ===")
    mydb = connect_db()

    # Test data: single songs
    single_songs = [
        ("Blinding Lights", ("Pop", "Synth-pop"), "The Weeknd", "2019-11-29"),
        ("Shape of You", ("Pop",), "Ed Sheeran", "2017-01-06"),
        ("Bohemian Rhapsody", ("Rock", "Opera"), "Queen", "1975-10-31"),
        ("Billie Jean", ("Pop", "R&B"), "Michael Jackson", "1983-01-02"),
        ("Hotel California", ("Rock",), "Eagles", "1977-02-22"),
        ("Smells Like Teen Spirit", ("Grunge", "Rock"), "Nirvana", "1991-09-10"),
        ("Imagine", ("Pop", "Rock"), "John Lennon", "1971-10-11"),
        ("Rolling in the Deep", ("Pop", "Soul"), "Adele", "2010-11-29"),
        ("Lose Yourself", ("Hip Hop", "Rap"), "Eminem", "2002-10-28"),
        ("Sweet Child O Mine", ("Rock",), "Guns N Roses", "1987-08-17"),
        ("Wonderwall", ("Rock", "Britpop"), "Oasis", "1995-10-30"),
        ("Someone Like You", ("Pop", "Soul"), "Adele", "2011-01-24"),
        ("Stairway to Heaven", ("Rock",), "Led Zeppelin", "1971-11-08"),
        ("Thriller", ("Pop", "Funk"), "Michael Jackson", "1984-01-23"),
        ("Hey Jude", ("Rock", "Pop"), "The Beatles", "1968-08-26"),
    ]

    rejected = load_single_songs(mydb, single_songs)
    print(f"✓ Loaded {len(single_songs) - len(rejected)} single songs")
    print(f"  Rejected: {rejected}")

    # Try to add duplicates
    duplicate_songs = [
        ("Blinding Lights", ("Pop",), "The Weeknd", "2020-01-01"),  # Duplicate
        ("New Song", ("Jazz",), "The Weeknd", "2020-05-15"),  # New song, same artist
    ]
    rejected2 = load_single_songs(mydb, duplicate_songs)
    print(f"✓ Duplicate test: rejected {rejected2}")

    mydb.close()


def test_get_most_prolific_individual_artists():
    """Test getting most prolific individual artists"""
    print("\n=== Testing get_most_prolific_individual_artists ===")
    mydb = connect_db()

    # Add more singles for testing
    more_singles = [
        ("Bad Guy", ("Pop", "Electropop"), "Billie Eilish", "2019-03-29"),
        ("Everything I Wanted", ("Alternative",), "Billie Eilish", "2019-11-13"),
        ("Therefore I Am", ("Pop",), "Billie Eilish", "2020-11-12"),
        ("Happier Than Ever", ("Pop",), "Billie Eilish", "2021-07-30"),
        ("Watermelon Sugar", ("Pop", "Rock"), "Harry Styles", "2019-11-16"),
        ("Golden", ("Pop",), "Harry Styles", "2019-10-26"),
        ("Adore You", ("Pop",), "Harry Styles", "2019-12-06"),
    ]
    load_single_songs(mydb, more_singles)

    # Get top 5 artists from 2019-2021
    top_artists = get_most_prolific_individual_artists(mydb, 5, (2019, 2021))
    print(f"✓ Top 5 most prolific artists (2019-2021):")
    for artist, count in top_artists:
        print(f"  {artist}: {count} singles")

    mydb.close()


def test_get_artists_last_single_in_year():
    """Test getting artists whose last single was in a given year"""
    print("\n=== Testing get_artists_last_single_in_year ===")
    mydb = connect_db()

    artists_2021 = get_artists_last_single_in_year(mydb, 2021)
    print(f"✓ Artists with last single in 2021: {artists_2021}")

    artists_2010 = get_artists_last_single_in_year(mydb, 2010)
    print(f"✓ Artists with last single in 2010: {artists_2010}")

    mydb.close()


def test_load_albums():
    """Test loading albums"""
    print("\n=== Testing load_albums ===")
    mydb = connect_db()

    albums = [
        (
            "25",
            "Pop",
            "Adele",
            "2015-11-20",
            [
                "Hello",
                "Send My Love",
                "When We Were Young",
                "Remedy",
                "Water Under the Bridge",
            ],
        ),
        (
            "Thriller Album",
            "Pop",
            "Michael Jackson",
            "1982-11-30",
            [
                "Wanna Be Startin Somethin",
                "Baby Be Mine",
                "The Girl Is Mine",
                "Thriller Song",
                "Beat It",
            ],
        ),
        (
            "Fine Line",
            "Pop",
            "Harry Styles",
            "2019-12-13",
            [
                "Golden Album",
                "Watermelon Sugar Album",
                "Adore You Album",
                "Lights Up",
                "Cherry",
            ],
        ),
        (
            "Abbey Road",
            "Rock",
            "The Beatles",
            "1969-09-26",
            [
                "Come Together",
                "Something",
                "Maxwell Silver Hammer",
                "Oh Darling",
                "Octopus Garden",
            ],
        ),
        (
            "Dark Side of the Moon",
            "Progressive Rock",
            "Pink Floyd",
            "1973-03-01",
            ["Speak to Me", "Breathe", "On the Run", "Time", "Money"],
        ),
        (
            "Back in Black",
            "Rock",
            "AC/DC",
            "1980-07-25",
            [
                "Hells Bells",
                "Shoot to Thrill",
                "What Do You Do for Money Honey",
                "Given the Dog a Bone",
                "Let Me Put My Love into You",
            ],
        ),
    ]

    rejected = load_albums(mydb, albums)
    print(f"✓ Loaded {len(albums) - len(rejected)} albums")
    print(f"  Rejected: {rejected}")

    # Try to add duplicate album
    duplicate_album = [
        ("25", "Soul", "Adele", "2015-11-20", ["Duplicate Song"])  # Duplicate album
    ]
    rejected2 = load_albums(mydb, duplicate_album)
    print(f"✓ Duplicate test: rejected {rejected2}")

    mydb.close()


def test_get_top_song_genres():
    """Test getting top song genres"""
    print("\n=== Testing get_top_song_genres ===")
    mydb = connect_db()

    top_genres = get_top_song_genres(mydb, 5)
    print(f"✓ Top 5 genres by number of songs:")
    for genre, count in top_genres:
        print(f"  {genre}: {count} songs")

    mydb.close()


def test_get_album_and_single_artists():
    """Test getting artists with both albums and singles"""
    print("\n=== Testing get_album_and_single_artists ===")
    mydb = connect_db()

    artists = get_album_and_single_artists(mydb)
    print(f"✓ Artists with both albums and singles:")
    for artist in sorted(artists):
        print(f"  {artist}")

    mydb.close()


def test_load_users():
    """Test loading users"""
    print("\n=== Testing load_users ===")
    mydb = connect_db()

    users = [
        "alice_music",
        "bob_rocks",
        "charlie_pop",
        "diana_jazz",
        "eve_listener",
        "frank_fan",
        "grace_melody",
        "henry_beats",
        "iris_song",
        "jack_tunes",
    ]

    rejected = load_users(mydb, users)
    print(f"✓ Loaded {len(users) - len(rejected)} users")
    print(f"  Rejected: {rejected}")

    # Try to add duplicates
    duplicate_users = ["alice_music", "bob_rocks", "new_user"]
    rejected2 = load_users(mydb, duplicate_users)
    print(f"✓ Duplicate test: rejected {rejected2}")

    mydb.close()


def test_load_song_ratings():
    """Test loading song ratings"""
    print("\n=== Testing load_song_ratings ===")
    mydb = connect_db()

    # Valid ratings
    ratings = [
        ("alice_music", ("The Weeknd", "Blinding Lights"), 5, "2020-01-15"),
        ("alice_music", ("Ed Sheeran", "Shape of You"), 4, "2020-02-10"),
        ("alice_music", ("Adele", "Rolling in the Deep"), 5, "2020-03-20"),
        ("bob_rocks", ("Queen", "Bohemian Rhapsody"), 5, "2020-01-20"),
        ("bob_rocks", ("Nirvana", "Smells Like Teen Spirit"), 5, "2020-02-15"),
        ("bob_rocks", ("Led Zeppelin", "Stairway to Heaven"), 5, "2020-03-10"),
        ("charlie_pop", ("The Weeknd", "Blinding Lights"), 4, "2020-01-25"),
        ("charlie_pop", ("Michael Jackson", "Billie Jean"), 5, "2020-02-20"),
        ("diana_jazz", ("Adele", "Hello"), 5, "2020-04-01"),
        ("diana_jazz", ("Adele", "Send My Love"), 4, "2020-04-02"),
        ("eve_listener", ("Harry Styles", "Watermelon Sugar"), 4, "2021-01-15"),
        ("eve_listener", ("Billie Eilish", "Bad Guy"), 5, "2021-02-10"),
        ("frank_fan", ("The Beatles", "Hey Jude"), 5, "2021-03-05"),
        ("grace_melody", ("Adele", "Someone Like You"), 5, "2021-04-12"),
        ("henry_beats", ("Eminem", "Lose Yourself"), 5, "2021-05-18"),
        ("iris_song", ("Michael Jackson", "Thriller"), 4, "2021-06-22"),
        ("jack_tunes", ("Eagles", "Hotel California"), 5, "2021-07-30"),
    ]

    rejected = load_song_ratings(mydb, ratings)
    print(f"✓ Loaded {len(ratings) - len(rejected)} ratings")
    print(f"  Rejected: {rejected}")

    # Invalid ratings (duplicates, non-existent users/songs, invalid rating values)
    invalid_ratings = [
        (
            "alice_music",
            ("The Weeknd", "Blinding Lights"),
            5,
            "2020-01-16",
        ),  # Duplicate
        (
            "nonexistent_user",
            ("Queen", "Bohemian Rhapsody"),
            5,
            "2020-01-20",
        ),  # User doesn't exist
        (
            "bob_rocks",
            ("Fake Artist", "Fake Song"),
            5,
            "2020-01-20",
        ),  # Song doesn't exist
        (
            "charlie_pop",
            ("Ed Sheeran", "Shape of You"),
            6,
            "2020-01-20",
        ),  # Rating out of range
        (
            "diana_jazz",
            ("Queen", "Bohemian Rhapsody"),
            0,
            "2020-01-20",
        ),  # Rating out of range
    ]

    rejected2 = load_song_ratings(mydb, invalid_ratings)
    print(f"✓ Invalid ratings test: rejected {rejected2}")

    mydb.close()


def test_get_most_rated_songs():
    """Test getting most rated songs"""
    print("\n=== Testing get_most_rated_songs ===")
    mydb = connect_db()

    # Add more ratings to make the test more interesting
    more_ratings = [
        ("bob_rocks", ("The Weeknd", "Blinding Lights"), 4, "2020-06-15"),
        ("charlie_pop", ("Adele", "Rolling in the Deep"), 4, "2020-07-20"),
        ("diana_jazz", ("The Weeknd", "Blinding Lights"), 5, "2020-08-25"),
        ("eve_listener", ("Queen", "Bohemian Rhapsody"), 5, "2020-09-30"),
        ("frank_fan", ("The Weeknd", "Blinding Lights"), 5, "2020-10-15"),
        ("grace_melody", ("Ed Sheeran", "Shape of You"), 4, "2020-11-20"),
        ("henry_beats", ("The Weeknd", "Blinding Lights"), 4, "2020-12-25"),
    ]
    load_song_ratings(mydb, more_ratings)

    most_rated = get_most_rated_songs(mydb, (2020, 2021), 10)
    print(f"✓ Top 10 most rated songs (2020-2021):")
    for song, artist, count in most_rated:
        print(f"  {song} by {artist}: {count} ratings")

    mydb.close()


def test_get_most_engaged_users():
    """Test getting most engaged users"""
    print("\n=== Testing get_most_engaged_users ===")
    mydb = connect_db()

    most_engaged = get_most_engaged_users(mydb, (2020, 2021), 5)
    print(f"✓ Top 5 most engaged users (2020-2021):")
    for username, count in most_engaged:
        print(f"  {username}: {count} songs rated")

    mydb.close()


def run_all_tests():
    """Run all tests in sequence"""
    print("=" * 60)
    print("MUSIC DATABASE TEST SUITE")
    print("=" * 60)

    try:
        # Test 1: Clear database
        test_clear_database()

        # Test 2: Load single songs
        test_load_single_songs()

        # Test 3: Get most prolific individual artists
        test_get_most_prolific_individual_artists()

        # Test 4: Get artists whose last single was in a given year
        test_get_artists_last_single_in_year()

        # Test 5: Load albums
        test_load_albums()

        # Test 6: Get top song genres
        test_get_top_song_genres()

        # Test 7: Get artists with both albums and singles
        test_get_album_and_single_artists()

        # Test 8: Load users
        test_load_users()

        # Test 9: Load song ratings
        test_load_song_ratings()

        # Test 10: Get most rated songs
        test_get_most_rated_songs()

        # Test 11: Get most engaged users
        test_get_most_engaged_users()

        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("\nBefore running this test suite:")
    print("1. Make sure MySQL is running")
    print("2. Update DB_CONFIG with your database credentials")
    print("3. Create the database schema using schema.sql")
    print("4. Run this script: python test_music_db.py")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()

    run_all_tests()
