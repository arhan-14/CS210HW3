"""
Unit tests with assertions for music database functions.
This file contains comprehensive tests with assertions to validate all functionality.

Prerequisites:
1. Run test_music_db.py first to populate the database
2. Make sure MySQL is running and DB_CONFIG matches your setup
"""

import os
import sys
import unittest
import mysql.connector

# Make sure the project root (where music_db.py lives) is on sys.path
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


class TestMusicDatabase(unittest.TestCase):
    """Test suite for music database functions"""

    @classmethod
    def setUpClass(cls):
        """Set up test database connection"""
        cls.db_config = DB_CONFIG
        print("\n" + "=" * 70)
        print("MUSIC DATABASE ASSERTION TEST SUITE")
        print("=" * 70)
        print("Note: Make sure you've run test_music_db.py first to populate data")
        print("=" * 70)

    def setUp(self):
        """Connect to database before each test"""
        self.mydb = mysql.connector.connect(**self.db_config)

    def tearDown(self):
        """Close database connection after each test"""
        self.mydb.close()

    def test_01_database_tables_exist(self):
        """Test that all required tables exist"""
        print("\n[TEST 1] Verifying database tables exist...")
        cursor = self.mydb.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()

        required_tables = [
            "Artists",
            "Genres",
            "Users",
            "Albums",
            "Songs",
            "SongGenres",
            "Ratings",
        ]

        for table in required_tables:
            self.assertIn(
                table, tables, f"Required table '{table}' is missing from database"
            )

        print(f"✓ All {len(required_tables)} required tables exist")

    def test_02_singles_loaded(self):
        """Test that single songs were loaded correctly"""
        print("\n[TEST 2] Verifying single songs are loaded...")
        cursor = self.mydb.cursor()

        # Count singles (songs with album_id NULL)
        cursor.execute("SELECT COUNT(*) FROM Songs WHERE album_id IS NULL")
        singles_count = cursor.fetchone()[0]

        # Should have at least 15 singles from test data
        self.assertGreaterEqual(
            singles_count, 15, "Should have at least 15 single songs"
        )
        print(f"✓ Found {singles_count} single songs in database")

        # Check specific song exists
        cursor.execute(
            """
            SELECT s.song_title, a.artist_name 
            FROM Songs s 
            JOIN Artists a ON s.artist_id = a.artist_id
            WHERE s.song_title = 'Blinding Lights' AND a.artist_name = 'The Weeknd'
        """
        )
        result = cursor.fetchone()
        self.assertIsNotNone(result, "Test song 'Blinding Lights' should exist")
        print(f"✓ Verified specific song: {result[0]} by {result[1]}")

        cursor.close()

    def test_03_albums_loaded(self):
        """Test that albums were loaded correctly"""
        print("\n[TEST 3] Verifying albums are loaded...")
        cursor = self.mydb.cursor()

        # Count albums
        cursor.execute("SELECT COUNT(*) FROM Albums")
        albums_count = cursor.fetchone()[0]

        self.assertGreaterEqual(albums_count, 6, "Should have at least 6 albums")
        print(f"✓ Found {albums_count} albums in database")

        # Count album songs (songs with album_id NOT NULL)
        cursor.execute("SELECT COUNT(*) FROM Songs WHERE album_id IS NOT NULL")
        album_songs_count = cursor.fetchone()[0]

        self.assertGreaterEqual(
            album_songs_count, 30, "Should have at least 30 album songs"
        )
        print(f"✓ Found {album_songs_count} songs in albums")

        # Verify specific album
        cursor.execute(
            """
            SELECT al.album_name, a.artist_name, COUNT(s.song_id) as song_count
            FROM Albums al
            JOIN Artists a ON al.artist_id = a.artist_id
            JOIN Songs s ON s.album_id = al.album_id
            WHERE al.album_name = '25'
            GROUP BY al.album_id
        """
        )
        result = cursor.fetchone()
        self.assertIsNotNone(result, "Test album '25' should exist")
        self.assertEqual(result[1], "Adele", "Album '25' should be by Adele")
        print(f"✓ Verified album: {result[0]} by {result[1]} ({result[2]} songs)")

        cursor.close()

    def test_04_genres_and_song_genres(self):
        """Test that genres and song-genre relationships exist"""
        print("\n[TEST 4] Verifying genres and song-genre relationships...")
        cursor = self.mydb.cursor()

        # Count genres
        cursor.execute("SELECT COUNT(*) FROM Genres")
        genres_count = cursor.fetchone()[0]

        self.assertGreaterEqual(genres_count, 5, "Should have at least 5 genres")
        print(f"✓ Found {genres_count} genres in database")

        # Count song-genre relationships
        cursor.execute("SELECT COUNT(*) FROM SongGenres")
        song_genres_count = cursor.fetchone()[0]

        self.assertGreater(
            song_genres_count, 0, "Should have song-genre relationships"
        )
        print(f"✓ Found {song_genres_count} song-genre relationships")

        # Verify a song can have multiple genres
        cursor.execute(
            """
            SELECT s.song_title, COUNT(sg.genre_id) as genre_count
            FROM Songs s
            JOIN SongGenres sg ON s.song_id = sg.song_id
            GROUP BY s.song_id
            HAVING genre_count > 1
            LIMIT 1
        """
        )
        result = cursor.fetchone()
        if result:
            print(f"✓ Verified multi-genre support: '{result[0]}' has {result[1]} genres")

        cursor.close()

    def test_05_users_loaded(self):
        """Test that users were loaded correctly"""
        print("\n[TEST 5] Verifying users are loaded...")
        cursor = self.mydb.cursor()

        # Count users
        cursor.execute("SELECT COUNT(*) FROM Users")
        users_count = cursor.fetchone()[0]

        self.assertGreaterEqual(users_count, 10, "Should have at least 10 users")
        print(f"✓ Found {users_count} users in database")

        # Verify specific user
        cursor.execute("SELECT user_name FROM Users WHERE user_name = 'alice_music'")
        result = cursor.fetchone()
        self.assertIsNotNone(result, "Test user 'alice_music' should exist")
        print(f"✓ Verified user: {result[0]}")

        cursor.close()

    def test_06_ratings_loaded(self):
        """Test that ratings were loaded correctly"""
        print("\n[TEST 6] Verifying ratings are loaded...")
        cursor = self.mydb.cursor()

        # Count ratings
        cursor.execute("SELECT COUNT(*) FROM Ratings")
        ratings_count = cursor.fetchone()[0]

        self.assertGreaterEqual(ratings_count, 15, "Should have at least 15 ratings")
        print(f"✓ Found {ratings_count} ratings in database")

        # Verify rating values are in valid range (1-5)
        cursor.execute("SELECT MIN(rating), MAX(rating) FROM Ratings")
        min_rating, max_rating = cursor.fetchone()

        self.assertGreaterEqual(min_rating, 1, "Minimum rating should be >= 1")
        self.assertLessEqual(max_rating, 5, "Maximum rating should be <= 5")
        print(f"✓ All ratings are in valid range: {min_rating} to {max_rating}")

        cursor.close()

    def test_07_get_most_prolific_artists(self):
        """Test get_most_prolific_individual_artists function"""
        print("\n[TEST 7] Testing get_most_prolific_individual_artists...")

        # Test for year range 2015-2021
        results = get_most_prolific_individual_artists(self.mydb, 5, (2015, 2021))

        self.assertIsInstance(results, list, "Should return a list")
        self.assertGreaterEqual(len(results), 1, "Should return at least 1 artist")
        self.assertLessEqual(len(results), 5, "Should return at most 5 artists")

        # Verify structure of results
        for artist_name, count in results:
            self.assertIsInstance(artist_name, str, "Artist name should be a string")
            self.assertIsInstance(count, int, "Count should be an integer")
            self.assertGreater(count, 0, "Count should be positive")

        # Verify ordering (descending by count, then alphabetically)
        if len(results) >= 2:
            for i in range(len(results) - 1):
                name1, count1 = results[i]
                name2, count2 = results[i + 1]
                if count1 == count2:
                    self.assertLess(
                        name1,
                        name2,
                        "Ties should be broken alphabetically by artist name",
                    )
                else:
                    self.assertGreaterEqual(
                        count1, count2, "Results should be ordered by count descending"
                    )

        print(f"✓ Top artists (2015-2021):")
        for artist_name, count in results[:3]:
            print(f"  - {artist_name}: {count} singles")

    def test_08_get_artists_last_single_in_year(self):
        """Test get_artists_last_single_in_year function"""
        print("\n[TEST 8] Testing get_artists_last_single_in_year...")

        # Test for year 2019
        results = get_artists_last_single_in_year(self.mydb, 2019)

        self.assertIsInstance(results, set, "Should return a set")

        # All results should be strings
        for artist_name in results:
            self.assertIsInstance(artist_name, str, "Artist names should be strings")

        print(f"✓ Found {len(results)} artists with last single in 2019")
        if results:
            print(f"  - Examples: {list(results)[:3]}")

    def test_09_get_top_song_genres(self):
        """Test get_top_song_genres function"""
        print("\n[TEST 9] Testing get_top_song_genres...")

        results = get_top_song_genres(self.mydb, 5)

        self.assertIsInstance(results, list, "Should return a list")
        self.assertGreaterEqual(len(results), 1, "Should return at least 1 genre")
        self.assertLessEqual(len(results), 5, "Should return at most 5 genres")

        # Verify structure and ordering
        for genre_name, count in results:
            self.assertIsInstance(genre_name, str, "Genre name should be a string")
            self.assertIsInstance(count, int, "Count should be an integer")
            self.assertGreater(count, 0, "Count should be positive")

        # Verify descending order by count
        if len(results) >= 2:
            for i in range(len(results) - 1):
                genre1, count1 = results[i]
                genre2, count2 = results[i + 1]
                if count1 == count2:
                    self.assertLess(
                        genre1, genre2, "Ties should be broken alphabetically"
                    )
                else:
                    self.assertGreaterEqual(
                        count1, count2, "Should be ordered by count descending"
                    )

        print(f"✓ Top {len(results)} genres:")
        for genre_name, count in results:
            print(f"  - {genre_name}: {count} songs")

    def test_10_get_album_and_single_artists(self):
        """Test get_album_and_single_artists function"""
        print("\n[TEST 10] Testing get_album_and_single_artists...")

        results = get_album_and_single_artists(self.mydb)

        self.assertIsInstance(results, set, "Should return a set")

        # All results should be strings
        for artist_name in results:
            self.assertIsInstance(artist_name, str, "Artist names should be strings")

        # Verify that these artists actually have both albums and singles
        if results:
            cursor = self.mydb.cursor()
            test_artist = list(results)[0]

            # Check for singles
            cursor.execute(
                """
                SELECT COUNT(*) FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                WHERE a.artist_name = %s AND s.album_id IS NULL
            """,
                (test_artist,),
            )
            singles_count = cursor.fetchone()[0]

            # Check for album songs
            cursor.execute(
                """
                SELECT COUNT(*) FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                WHERE a.artist_name = %s AND s.album_id IS NOT NULL
            """,
                (test_artist,),
            )
            album_songs_count = cursor.fetchone()[0]

            self.assertGreater(
                singles_count, 0, f"{test_artist} should have at least 1 single"
            )
            self.assertGreater(
                album_songs_count, 0, f"{test_artist} should have at least 1 album song"
            )

            cursor.close()

        print(f"✓ Found {len(results)} artists with both albums and singles")
        if results:
            print(f"  - Examples: {list(results)[:3]}")

    def test_11_get_most_rated_songs(self):
        """Test get_most_rated_songs function"""
        print("\n[TEST 11] Testing get_most_rated_songs...")

        results = get_most_rated_songs(self.mydb, (2020, 2021), 10)

        self.assertIsInstance(results, list, "Should return a list")
        self.assertLessEqual(len(results), 10, "Should return at most 10 songs")

        # Verify structure and ordering
        for song_title, artist_name, count in results:
            self.assertIsInstance(song_title, str, "Song title should be a string")
            self.assertIsInstance(artist_name, str, "Artist name should be a string")
            self.assertIsInstance(count, int, "Count should be an integer")
            self.assertGreater(count, 0, "Count should be positive")

        # Verify descending order by count
        if len(results) >= 2:
            for i in range(len(results) - 1):
                song1, artist1, count1 = results[i]
                song2, artist2, count2 = results[i + 1]
                if count1 == count2:
                    self.assertLessEqual(
                        song1,
                        song2,
                        "Ties should be broken alphabetically by song title",
                    )
                else:
                    self.assertGreaterEqual(
                        count1, count2, "Should be ordered by count descending"
                    )

        print(f"✓ Top {len(results)} most rated songs (2020-2021):")
        for song_title, artist_name, count in results[:5]:
            print(f"  - '{song_title}' by {artist_name}: {count} ratings")

    def test_12_get_most_engaged_users(self):
        """Test get_most_engaged_users function"""
        print("\n[TEST 12] Testing get_most_engaged_users...")

        results = get_most_engaged_users(self.mydb, (2020, 2021), 10)

        self.assertIsInstance(results, list, "Should return a list")
        self.assertLessEqual(len(results), 10, "Should return at most 10 users")

        # Verify structure and ordering
        for username, count in results:
            self.assertIsInstance(username, str, "Username should be a string")
            self.assertIsInstance(count, int, "Count should be an integer")
            self.assertGreater(count, 0, "Count should be positive")

        # Verify descending order by count
        if len(results) >= 2:
            for i in range(len(results) - 1):
                user1, count1 = results[i]
                user2, count2 = results[i + 1]
                if count1 == count2:
                    self.assertLess(
                        user1, user2, "Ties should be broken alphabetically by username"
                    )
                else:
                    self.assertGreaterEqual(
                        count1, count2, "Should be ordered by count descending"
                    )

        print(f"✓ Top {len(results)} most engaged users (2020-2021):")
        for username, count in results[:5]:
            print(f"  - {username}: {count} songs rated")

    def test_13_duplicate_rejection_singles(self):
        """Test that duplicate singles are properly rejected"""
        print("\n[TEST 13] Testing duplicate single song rejection...")

        # Try to add a duplicate single
        duplicate_songs = [
            ("Blinding Lights", ("Pop",), "The Weeknd", "2019-11-29"),
            ("New Unique Song", ("Rock",), "Test Artist", "2020-01-01"),
        ]

        rejected = load_single_songs(self.mydb, duplicate_songs)

        self.assertIn(
            ("Blinding Lights", "The Weeknd"),
            rejected,
            "Duplicate song should be rejected",
        )
        print(f"✓ Duplicate rejection working: {len(rejected)} duplicates rejected")

        # Clean up the new song (delete genre relationships first, then song)
        cursor = self.mydb.cursor()
        
        # First, delete from SongGenres
        cursor.execute(
            """
            DELETE sg FROM SongGenres sg
            JOIN Songs s ON sg.song_id = s.song_id
            WHERE s.song_title = 'New Unique Song'
        """
        )
        
        # Then delete the song
        cursor.execute(
            """
            DELETE FROM Songs 
            WHERE song_title = 'New Unique Song'
        """
        )
        
        self.mydb.commit()
        cursor.close()

    def test_14_duplicate_rejection_users(self):
        """Test that duplicate users are properly rejected"""
        print("\n[TEST 14] Testing duplicate user rejection...")

        # Try to add duplicate users
        test_users = ["alice_music", "new_test_user_xyz"]

        rejected = load_users(self.mydb, test_users)

        self.assertIn("alice_music", rejected, "Duplicate user should be rejected")
        print(f"✓ Duplicate user rejection working: {len(rejected)} duplicates rejected")

        # Clean up new user
        cursor = self.mydb.cursor()
        cursor.execute("DELETE FROM Users WHERE user_name = 'new_test_user_xyz'")
        self.mydb.commit()
        cursor.close()

    def test_15_rating_validation(self):
        """Test rating validation (invalid ratings, users, songs)"""
        print("\n[TEST 15] Testing rating validation...")

        test_ratings = [
            ("alice_music", ("The Weeknd", "Blinding Lights"), 6, "2021-01-01"),  # Invalid: rating > 5
            ("alice_music", ("Ed Sheeran", "Shape of You"), 0, "2021-01-02"),  # Invalid: rating < 1
            ("nonexistent_user_xyz123", ("Queen", "Bohemian Rhapsody"), 5, "2021-01-03"),  # Invalid: user doesn't exist
            ("alice_music", ("Fake Artist", "Fake Song"), 5, "2021-01-04"),  # Invalid: song doesn't exist
        ]

        rejected = load_song_ratings(self.mydb, test_ratings)

        self.assertEqual(
            len(rejected), 4, "All 4 invalid ratings should be rejected"
        )
        print(f"✓ Rating validation working: {len(rejected)} invalid ratings rejected")

    def test_16_data_integrity(self):
        """Test database referential integrity"""
        print("\n[TEST 16] Testing data integrity...")

        cursor = self.mydb.cursor()

        # Check that all songs have valid artist_id
        cursor.execute(
            """
            SELECT COUNT(*) FROM Songs s
            LEFT JOIN Artists a ON s.artist_id = a.artist_id
            WHERE a.artist_id IS NULL
        """
        )
        orphaned_songs = cursor.fetchone()[0]
        self.assertEqual(orphaned_songs, 0, "No songs should have invalid artist_id")

        # Check that all album songs have valid album_id
        cursor.execute(
            """
            SELECT COUNT(*) FROM Songs s
            LEFT JOIN Albums al ON s.album_id = al.album_id
            WHERE s.album_id IS NOT NULL AND al.album_id IS NULL
        """
        )
        orphaned_album_songs = cursor.fetchone()[0]
        self.assertEqual(
            orphaned_album_songs, 0, "No album songs should have invalid album_id"
        )

        # Check that all ratings have valid user_id and song_id
        cursor.execute(
            """
            SELECT COUNT(*) FROM Ratings r
            LEFT JOIN Users u ON r.user_id = u.user_id
            LEFT JOIN Songs s ON r.song_id = s.song_id
            WHERE u.user_id IS NULL OR s.song_id IS NULL
        """
        )
        orphaned_ratings = cursor.fetchone()[0]
        self.assertEqual(
            orphaned_ratings, 0, "No ratings should have invalid user_id or song_id"
        )

        cursor.close()
        print("✓ All referential integrity checks passed")

    def test_17_empty_results_handling(self):
        """Test that functions handle empty results correctly"""
        print("\n[TEST 17] Testing empty result handling...")

        # Test with future year range where no data exists
        future_artists = get_most_prolific_individual_artists(
            self.mydb, 5, (2030, 2035)
        )
        self.assertIsInstance(future_artists, list, "Should return empty list")
        self.assertEqual(len(future_artists), 0, "Should return empty list for future years")

        future_ratings = get_most_rated_songs(self.mydb, (2030, 2035), 10)
        self.assertIsInstance(future_ratings, list, "Should return empty list")
        self.assertEqual(len(future_ratings), 0, "Should return empty list for future years")

        future_users = get_most_engaged_users(self.mydb, (2030, 2035), 10)
        self.assertIsInstance(future_users, list, "Should return empty list")
        self.assertEqual(len(future_users), 0, "Should return empty list for future years")

        print("✓ Empty result handling works correctly")


def run_tests():
    """Run all tests with unittest"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMusicDatabase)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✓ ALL TESTS PASSED!")
    else:
        print("\n✗ SOME TESTS FAILED")

    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("\nBefore running these assertion tests:")
    print("1. Make sure you've run test_music_db.py first to populate data")
    print("2. Make sure MySQL is running")
    print("3. Update DB_CONFIG with your database credentials")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()

    success = run_tests()
    exit(0 if success else 1)
