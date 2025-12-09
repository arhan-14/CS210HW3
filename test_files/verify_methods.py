import os
import sys
import mysql.connector

# Ensure music_db.py (project root) is importable when running from test_files/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from music_db import *

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "musicdb",
}

mydb = mysql.connector.connect(**DB_CONFIG)

print("=" * 60)
print("VERIFYING METHOD BEHAVIOR")
print("=" * 60)

# Test 1: Duplicate song rejection
print("\n1. Testing duplicate single song rejection:")
print("   Trying to add 'Blinding Lights' by The Weeknd (already exists)")
duplicate = [("Blinding Lights", ("Pop",), "The Weeknd", "2019-11-29")]
rejected = load_single_songs(mydb, duplicate)
print(f"   Result: {rejected}")
print(
    f"   ✓ CORRECT: Duplicate was rejected"
    if rejected
    else "   ✗ ERROR: Should have been rejected!"
)

# Test 2: Invalid rating (rating > 5)
print("\n2. Testing invalid rating (rating=6):")
print("   Trying to add rating of 6 for a song")
invalid_rating = [("alice_music", ("The Weeknd", "Blinding Lights"), 6, "2021-01-01")]
rejected = load_song_ratings(mydb, invalid_rating)
print(f"   Result: {rejected}")
print(
    f"   ✓ CORRECT: Invalid rating rejected"
    if rejected
    else "   ✗ ERROR: Should have been rejected!"
)

# Test 3: Invalid rating (rating < 1)
print("\n3. Testing invalid rating (rating=0):")
print("   Trying to add rating of 0 for a song")
invalid_rating = [("alice_music", ("Ed Sheeran", "Shape of You"), 0, "2021-01-01")]
rejected = load_song_ratings(mydb, invalid_rating)
print(f"   Result: {rejected}")
print(
    f"   ✓ CORRECT: Invalid rating rejected"
    if rejected
    else "   ✗ ERROR: Should have been rejected!"
)

# Test 4: Nonexistent user
print("\n4. Testing nonexistent user:")
print("   Trying to add rating from user that doesn't exist")
invalid_rating = [("fake_user_12345", ("Queen", "Bohemian Rhapsody"), 5, "2021-01-01")]
rejected = load_song_ratings(mydb, invalid_rating)
print(f"   Result: {rejected}")
print(
    f"   ✓ CORRECT: Rejected" if rejected else "   ✗ ERROR: Should have been rejected!"
)

# Test 5: Nonexistent song
print("\n5. Testing nonexistent song:")
print("   Trying to add rating for song that doesn't exist")
invalid_rating = [("alice_music", ("Fake Artist", "Fake Song"), 5, "2021-01-01")]
rejected = load_song_ratings(mydb, invalid_rating)
print(f"   Result: {rejected}")
print(
    f"   ✓ CORRECT: Rejected" if rejected else "   ✗ ERROR: Should have been rejected!"
)

# Test 6: Duplicate user
print("\n6. Testing duplicate user:")
print("   Trying to add user 'alice_music' (already exists)")
duplicate_user = ["alice_music"]
rejected = load_users(mydb, duplicate_user)
print(f"   Result: {rejected}")
print(
    f"   ✓ CORRECT: Duplicate rejected"
    if rejected
    else "   ✗ ERROR: Should have been rejected!"
)

# Test 7: Get most prolific artists
print("\n7. Testing get_most_prolific_individual_artists:")
results = get_most_prolific_individual_artists(mydb, 3, (2015, 2021))
print(f"   Top 3 artists (2015-2021):")
for artist, count in results:
    print(f"     - {artist}: {count} singles")
print(f"   ✓ Returns list: {isinstance(results, list)}")
print(
    f"   ✓ Ordered descending: {all(results[i][1] >= results[i+1][1] for i in range(len(results)-1))}"
)

# Test 8: Get top genres
print("\n8. Testing get_top_song_genres:")
results = get_top_song_genres(mydb, 3)
print(f"   Top 3 genres:")
for genre, count in results:
    print(f"     - {genre}: {count} songs")
print(f"   ✓ Returns list: {isinstance(results, list)}")

# Test 9: Get album and single artists
print("\n9. Testing get_album_and_single_artists:")
results = get_album_and_single_artists(mydb)
print(f"   Artists with both: {results}")
print(f"   ✓ Returns set: {isinstance(results, set)}")

# Test 10: Get most rated songs
print("\n10. Testing get_most_rated_songs:")
results = get_most_rated_songs(mydb, (2020, 2021), 3)
print(f"   Top 3 rated songs (2020-2021):")
for song, artist, count in results:
    print(f"     - '{song}' by {artist}: {count} ratings")
print(f"   ✓ Returns list: {isinstance(results, list)}")

mydb.close()
print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
