"""
Quick assertion tests for music database.
Simpler version of test_assertions.py for rapid testing.

Run this after test_music_db.py has populated the database.
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
    "password": "root",
    "database": "musicdb",
}


def assert_test(condition, test_name, success_msg="✓ Passed", fail_msg="✗ Failed"):
    """Simple assertion helper"""
    if condition:
        print(f"{success_msg}: {test_name}")
        return True
    else:
        print(f"{fail_msg}: {test_name}")
        return False


def run_quick_tests():
    """Run quick assertion tests"""
    print("\n" + "=" * 60)
    print("QUICK ASSERTION TESTS")
    print("=" * 60)

    mydb = mysql.connector.connect(**DB_CONFIG)
    cursor = mydb.cursor()
    passed = 0
    total = 0

    # Test 1: Singles exist
    total += 1
    cursor.execute("SELECT COUNT(*) FROM Songs WHERE album_id IS NULL")
    singles_count = cursor.fetchone()[0]
    if assert_test(
        singles_count >= 15, "Singles loaded", f"✓ {singles_count} singles found"
    ):
        passed += 1

    # Test 2: Albums exist
    total += 1
    cursor.execute("SELECT COUNT(*) FROM Albums")
    albums_count = cursor.fetchone()[0]
    if assert_test(
        albums_count >= 6, "Albums loaded", f"✓ {albums_count} albums found"
    ):
        passed += 1

    # Test 3: Users exist
    total += 1
    cursor.execute("SELECT COUNT(*) FROM Users")
    users_count = cursor.fetchone()[0]
    if assert_test(users_count >= 10, "Users loaded", f"✓ {users_count} users found"):
        passed += 1

    # Test 4: Ratings exist
    total += 1
    cursor.execute("SELECT COUNT(*) FROM Ratings")
    ratings_count = cursor.fetchone()[0]
    if assert_test(
        ratings_count >= 15, "Ratings loaded", f"✓ {ratings_count} ratings found"
    ):
        passed += 1

    # Test 5: Ratings are in valid range
    total += 1
    cursor.execute("SELECT MIN(rating), MAX(rating) FROM Ratings")
    min_r, max_r = cursor.fetchone()
    if assert_test(
        min_r >= 1 and max_r <= 5,
        "Rating range (1-5)",
        f"✓ Ratings range: {min_r} to {max_r}",
    ):
        passed += 1

    # Test 6: get_most_prolific_individual_artists returns results
    total += 1
    results = get_most_prolific_individual_artists(mydb, 5, (2015, 2021))
    if assert_test(
        len(results) > 0 and len(results) <= 5,
        "get_most_prolific_individual_artists",
        f"✓ Returned {len(results)} artists",
    ):
        passed += 1

    # Test 7: Results are properly ordered (descending)
    total += 1
    is_ordered = all(
        results[i][1] >= results[i + 1][1] for i in range(len(results) - 1)
    )
    if assert_test(is_ordered, "Prolific artists ordering", "✓ Properly ordered"):
        passed += 1

    # Test 8: get_top_song_genres returns results
    total += 1
    genre_results = get_top_song_genres(mydb, 5)
    if assert_test(
        len(genre_results) > 0,
        "get_top_song_genres",
        f"✓ Returned {len(genre_results)} genres",
    ):
        passed += 1

    # Test 9: Genre counts are positive
    total += 1
    all_positive = all(count > 0 for _, count in genre_results)
    if assert_test(
        all_positive, "Genre counts positive", "✓ All counts are positive"
    ):
        passed += 1

    # Test 10: get_album_and_single_artists returns set
    total += 1
    both_artists = get_album_and_single_artists(mydb)
    if assert_test(
        isinstance(both_artists, set),
        "get_album_and_single_artists type",
        f"✓ Returned set with {len(both_artists)} artists",
    ):
        passed += 1

    # Test 11: Verify an artist has both albums and singles
    total += 1
    if both_artists:
        test_artist = list(both_artists)[0]
        cursor.execute(
            """
            SELECT 
                SUM(CASE WHEN album_id IS NULL THEN 1 ELSE 0 END) as singles,
                SUM(CASE WHEN album_id IS NOT NULL THEN 1 ELSE 0 END) as album_songs
            FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            WHERE a.artist_name = %s
        """,
            (test_artist,),
        )
        singles, album_songs = cursor.fetchone()
        if assert_test(
            singles > 0 and album_songs > 0,
            f"Artist '{test_artist}' has both types",
            f"✓ {singles} singles, {album_songs} album songs",
        ):
            passed += 1
    else:
        total += 1

    # Test 12: get_most_rated_songs returns proper structure
    total += 1
    rated_songs = get_most_rated_songs(mydb, (2020, 2021), 5)
    valid_structure = all(
        len(item) == 3
        and isinstance(item[0], str)
        and isinstance(item[1], str)
        and isinstance(item[2], int)
        for item in rated_songs
    )
    if assert_test(
        valid_structure,
        "get_most_rated_songs structure",
        f"✓ Returned {len(rated_songs)} songs with valid structure",
    ):
        passed += 1

    # Test 13: get_most_engaged_users returns proper structure
    total += 1
    engaged_users = get_most_engaged_users(mydb, (2020, 2021), 5)
    valid_structure = all(
        len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], int)
        for item in engaged_users
    )
    if assert_test(
        valid_structure,
        "get_most_engaged_users structure",
        f"✓ Returned {len(engaged_users)} users with valid structure",
    ):
        passed += 1

    # Test 14: get_artists_last_single_in_year returns set
    total += 1
    last_single_2019 = get_artists_last_single_in_year(mydb, 2019)
    if assert_test(
        isinstance(last_single_2019, set),
        "get_artists_last_single_in_year type",
        f"✓ Returned set with {len(last_single_2019)} artists",
    ):
        passed += 1

    # Test 15: Duplicate song rejection
    total += 1
    duplicate_songs = [("Blinding Lights", ("Pop",), "The Weeknd", "2019-11-29")]
    rejected = load_single_songs(mydb, duplicate_songs)
    if assert_test(
        len(rejected) > 0,
        "Duplicate song rejection",
        f"✓ Rejected {len(rejected)} duplicate",
    ):
        passed += 1

    # Test 16: Duplicate user rejection
    total += 1
    duplicate_users = ["alice_music"]
    rejected_users = load_users(mydb, duplicate_users)
    if assert_test(
        len(rejected_users) > 0,
        "Duplicate user rejection",
        f"✓ Rejected {len(rejected_users)} duplicate",
    ):
        passed += 1

    # Test 17: Invalid rating rejection (rating > 5)
    total += 1
    invalid_ratings = [
        ("alice_music", ("The Weeknd", "Blinding Lights"), 6, "2021-01-01")
    ]
    rejected_ratings = load_song_ratings(mydb, invalid_ratings)
    if assert_test(
        len(rejected_ratings) > 0,
        "Invalid rating rejection (>5)",
        f"✓ Rejected {len(rejected_ratings)} invalid rating",
    ):
        passed += 1

    # Test 18: Invalid rating rejection (nonexistent user)
    total += 1
    invalid_ratings = [
        ("fake_user_xyz", ("The Weeknd", "Blinding Lights"), 5, "2021-01-01")
    ]
    rejected_ratings = load_song_ratings(mydb, invalid_ratings)
    if assert_test(
        len(rejected_ratings) > 0,
        "Invalid rating rejection (fake user)",
        f"✓ Rejected {len(rejected_ratings)} invalid rating",
    ):
        passed += 1

    # Test 19: Empty results handling
    total += 1
    future_results = get_most_prolific_individual_artists(mydb, 5, (2030, 2035))
    if assert_test(
        len(future_results) == 0,
        "Empty results for future year range",
        "✓ Returns empty list correctly",
    ):
        passed += 1

    # Test 20: Referential integrity - songs without artists
    total += 1
    cursor.execute(
        """
        SELECT COUNT(*) FROM Songs s
        LEFT JOIN Artists a ON s.artist_id = a.artist_id
        WHERE a.artist_id IS NULL
    """
    )
    orphaned = cursor.fetchone()[0]
    if assert_test(
        orphaned == 0, "Referential integrity (Songs->Artists)", "✓ No orphaned songs"
    ):
        passed += 1

    cursor.close()
    mydb.close()

    # Summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("✓ ALL TESTS PASSED!")
        return True
    else:
        print(f"✗ {total - passed} tests failed")
        return False


if __name__ == "__main__":
    print("Make sure you've run test_music_db.py first to populate the database!")
    print("Press Enter to continue...")
    input()

    success = run_quick_tests()
    exit(0 if success else 1)
