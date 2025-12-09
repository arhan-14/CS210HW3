# Music Database - CS210 HW3

This project implements a music database system with functions to manage songs, albums, artists, users, and ratings.

## Setup Instructions

### 1. Install MySQL

Make sure you have MySQL installed and running on your system.

### 2. Install Python MySQL Connector

```bash
pip install mysql-connector-python
```

### 3. Create the Database

```bash
# Log into MySQL
mysql -u root -p

# Create the database
CREATE DATABASE music_database;

# Use the database
USE music_database;

# Import the schema
SOURCE schema.sql;

# Exit MySQL
exit;
```

### 4. Configure Database Connection

Edit `test_music_db.py` and update the `DB_CONFIG` dictionary with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Change this
    'database': 'music_database'
}
```

## Running the Tests

### Step 1: Populate the Database

```bash
python test_music_db.py
```

This loads all test data into the database.

### Step 2: Run Assertion Tests

```bash
# Comprehensive unittest-based assertions
python test_assertions.py

# Quick assertion tests (faster)
python test_quick.py
```

The assertion tests validate:

- ✅ All data loaded correctly
- ✅ Functions return correct data types
- ✅ Results are properly ordered
- ✅ Duplicate rejection works
- ✅ Invalid data is rejected
- ✅ Empty results are handled
- ✅ Referential integrity is maintained

## Implemented Functions

### 1. `clear_database(mydb)`

Clears all data from all tables while respecting foreign key constraints.

### 2. `load_single_songs(mydb, single_songs)`

Loads single songs (not part of albums) into the database.

- Returns set of rejected (song, artist) tuples if they already exist

### 3. `get_most_prolific_individual_artists(mydb, n, year_range)`

Gets top n artists by number of singles released in a year range.

- Breaks ties alphabetically

### 4. `get_artists_last_single_in_year(mydb, year)`

Finds artists whose last single was released in the given year.

### 5. `load_albums(mydb, albums)`

Loads albums with their songs into the database.

- Returns set of rejected (album, artist) tuples if they already exist

### 6. `get_top_song_genres(mydb, n)`

Gets n most represented genres by total song count (singles + album songs).

- Breaks ties alphabetically

### 7. `get_album_and_single_artists(mydb)`

Finds artists who have released both albums and singles.

### 8. `load_users(mydb, users)`

Loads users into the database.

- Returns set of rejected usernames if they already exist

### 9. `load_song_ratings(mydb, song_ratings)`

Loads ratings for songs with validation.

- Rejects if: user doesn't exist, song doesn't exist, duplicate rating, or rating not in range 1-5
- Returns set of rejected (username, artist, song) tuples

### 10. `get_most_rated_songs(mydb, year_range, n)`

Gets top n songs by number of ratings (not rating score) in a year range.

- Breaks ties alphabetically by song title

### 11. `get_most_engaged_users(mydb, year_range, n)`

Gets top n users by number of songs they've rated in a year range.

- Breaks ties alphabetically by username

## Test Data Overview

The test suite includes:

### Singles

- 15+ popular songs from various artists and decades
- Multiple genres per song (Pop, Rock, Hip Hop, etc.)
- Artists: The Weeknd, Ed Sheeran, Queen, Michael Jackson, Adele, etc.

### Albums

- 6 iconic albums with 5 songs each
- Albums: "25" (Adele), "Thriller Album" (Michael Jackson), "Fine Line" (Harry Styles), etc.

### Users

- 10 test users: alice_music, bob_rocks, charlie_pop, etc.

### Ratings

- 20+ ratings across different songs and time periods
- Tests for duplicate detection, invalid users/songs, and out-of-range ratings

## Database Schema

The schema consists of 7 tables:

- **Artists**: artist_id, artist_name
- **Genres**: genre_id, genre_name
- **Users**: user_id, user_name
- **Albums**: album_id, album_name, artist_id, release_date, genre_id
- **Songs**: song_id, song_title, artist_id, album_id (NULL for singles), release_date
- **SongGenres**: song_id, genre_id (many-to-many relationship)
- **Ratings**: rating_id, user_id, song_id, rating, rating_date

## Key Design Decisions

1. **Singles vs Album Songs**: Singles have `album_id = NULL` in the Songs table
2. **Multiple Genres**: Songs can have multiple genres via the SongGenres junction table
3. **Unique Constraints**: (song_title, artist_id) is unique, as is (album_name, artist_id)
4. **Rating Range**: Ratings must be between 1 and 5 (inclusive)
5. **Duplicate Prevention**: All load functions return rejected items for transparency

## Notes

- All dates are in 'YYYY-MM-DD' format
- Foreign key constraints are handled properly during deletion
- Ties in rankings are broken alphabetically
- Functions return empty sets/lists when there are no results
