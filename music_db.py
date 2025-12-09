from typing import Tuple, List, Set


def clear_database(mydb):
    """
    Deletes all the rows from all the tables of the database.
    If a table has a foreign key to a parent table, it is deleted before
    deleting the parent table, otherwise the database system will throw an error.

    Args:
        mydb: database connection
    """
    cursor = mydb.cursor()

    # Delete in order respecting foreign key constraints
    # Child tables first, then parent tables
    cursor.execute("DELETE FROM Ratings")
    cursor.execute("DELETE FROM SongGenres")
    cursor.execute("DELETE FROM Songs")
    cursor.execute("DELETE FROM Albums")
    cursor.execute("DELETE FROM Users")
    cursor.execute("DELETE FROM Genres")
    cursor.execute("DELETE FROM Artists")

    mydb.commit()
    cursor.close()


def load_single_songs(
    mydb, single_songs: List[Tuple[str, Tuple[str, ...], str, str]]
) -> Set[Tuple[str, str]]:
    """
    Add single songs to the database.

    Args:
        mydb: database connection

        single_songs: List of single songs to add. Each single song is a tuple of the form:
              (song title, genre names, artist name, release date)
        Genre names is a tuple since a song could belong to multiple genres
        Release date is of the form yyyy-dd-mm
        Example 1 single song: ('S1',('Pop',),'A1','2008-10-01') => here song is of genre Pop
        Example 2 single song: ('S2',('Rock', 'Pop),'A2','2000-02-15') => here song is of genre Rock and Pop

    Returns:
        Set[Tuple[str,str]]: set of (song,artist) for combinations that already exist
        in the database and were not added (rejected).
        Set is empty if there are no rejects.
    """
    cursor = mydb.cursor()
    rejected = set()

    for song_title, genres, artist_name, release_date in single_songs:
        # Check if (song_title, artist) already exists
        cursor.execute(
            """
            SELECT s.song_id FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            WHERE s.song_title = %s AND a.artist_name = %s
        """,
            (song_title, artist_name),
        )

        if cursor.fetchone():
            rejected.add((song_title, artist_name))
            continue

        # Insert or get artist
        cursor.execute(
            "SELECT artist_id FROM Artists WHERE artist_name = %s", (artist_name,)
        )
        result = cursor.fetchone()
        if result:
            artist_id = result[0]
        else:
            cursor.execute(
                "INSERT INTO Artists (artist_name) VALUES (%s)", (artist_name,)
            )
            artist_id = cursor.lastrowid

        # Insert song (album_id is NULL for singles)
        cursor.execute(
            """
            INSERT INTO Songs (song_title, artist_id, album_id, release_date)
            VALUES (%s, %s, NULL, %s)
        """,
            (song_title, artist_id, release_date),
        )
        song_id = cursor.lastrowid

        # Insert genres and link to song
        for genre_name in genres:
            # Insert or get genre
            cursor.execute(
                "SELECT genre_id FROM Genres WHERE genre_name = %s", (genre_name,)
            )
            result = cursor.fetchone()
            if result:
                genre_id = result[0]
            else:
                cursor.execute(
                    "INSERT INTO Genres (genre_name) VALUES (%s)", (genre_name,)
                )
                genre_id = cursor.lastrowid

            # Link song to genre
            cursor.execute(
                """
                INSERT INTO SongGenres (song_id, genre_id)
                VALUES (%s, %s)
            """,
                (song_id, genre_id),
            )

    mydb.commit()
    cursor.close()
    return rejected


def get_most_prolific_individual_artists(
    mydb, n: int, year_range: Tuple[int, int]
) -> List[Tuple[str, int]]:
    """
    Get the top n most prolific individual artists by number of singles released in a year range.
    Break ties by alphabetical order of artist name.

    Args:
        mydb: database connection
        n: how many to get
        year_range: tuple, e.g. (2015,2020)

    Returns:
        List[Tuple[str,int]]: list of (artist name, number of songs) tuples.
        If there are fewer than n artists, all of them are returned.
        If there are no artists, an empty list is returned.
    """
    cursor = mydb.cursor()

    # Singles are songs with album_id NULL
    cursor.execute(
        """
        SELECT a.artist_name, COUNT(*) as num_singles
        FROM Songs s
        JOIN Artists a ON s.artist_id = a.artist_id
        WHERE s.album_id IS NULL
          AND YEAR(s.release_date) BETWEEN %s AND %s
        GROUP BY a.artist_id, a.artist_name
        ORDER BY num_singles DESC, a.artist_name ASC
        LIMIT %s
    """,
        (year_range[0], year_range[1], n),
    )

    results = [(row[0], row[1]) for row in cursor.fetchall()]
    cursor.close()
    return results


def get_artists_last_single_in_year(mydb, year: int) -> Set[str]:
    """
    Get all artists who released their last single in the given year.

    Args:
        mydb: database connection
        year: year of last release

    Returns:
        Set[str]: set of artist names
        If there is no artist with a single released in the given year, an empty set is returned.
    """
    cursor = mydb.cursor()

    # Find artists whose last single was in the given year
    cursor.execute(
        """
        SELECT a.artist_name
        FROM Artists a
        WHERE EXISTS (
            SELECT 1 FROM Songs s
            WHERE s.artist_id = a.artist_id
              AND s.album_id IS NULL
              AND YEAR(s.release_date) = %s
        )
        AND NOT EXISTS (
            SELECT 1 FROM Songs s2
            WHERE s2.artist_id = a.artist_id
              AND s2.album_id IS NULL
              AND YEAR(s2.release_date) > %s
        )
    """,
        (year, year),
    )

    results = {row[0] for row in cursor.fetchall()}
    cursor.close()
    return results


def load_albums(
    mydb, albums: List[Tuple[str, str, str, str, List[str]]]
) -> Set[Tuple[str, str]]:
    """
    Add albums to the database.

    Args:
        mydb: database connection

        albums: List of albums to add. Each album is a tuple of the form:
              (album title, genre, artist name, release date, list of song titles)
        Release date is of the form yyyy-dd-mm
        Example album: ('Album1','Jazz','A1','2008-10-01',['s1','s2','s3','s4','s5','s6'])

    Returns:
        Set[Tuple[str,str]: set of (album, artist) combinations that were not added (rejected)
        because the artist already has an album of the same title.
        Set is empty if there are no rejects.
    """
    cursor = mydb.cursor()
    rejected = set()

    for album_name, genre_name, artist_name, release_date, song_titles in albums:
        # Insert or get artist
        cursor.execute(
            "SELECT artist_id FROM Artists WHERE artist_name = %s", (artist_name,)
        )
        result = cursor.fetchone()
        if result:
            artist_id = result[0]
        else:
            cursor.execute(
                "INSERT INTO Artists (artist_name) VALUES (%s)", (artist_name,)
            )
            artist_id = cursor.lastrowid

        # Check if (album_name, artist) already exists
        cursor.execute(
            """
            SELECT album_id FROM Albums
            WHERE album_name = %s AND artist_id = %s
        """,
            (album_name, artist_id),
        )

        if cursor.fetchone():
            rejected.add((album_name, artist_name))
            continue

        # Insert or get genre
        cursor.execute(
            "SELECT genre_id FROM Genres WHERE genre_name = %s", (genre_name,)
        )
        result = cursor.fetchone()
        if result:
            genre_id = result[0]
        else:
            cursor.execute("INSERT INTO Genres (genre_name) VALUES (%s)", (genre_name,))
            genre_id = cursor.lastrowid

        # Insert album
        cursor.execute(
            """
            INSERT INTO Albums (album_name, artist_id, release_date, genre_id)
            VALUES (%s, %s, %s, %s)
        """,
            (album_name, artist_id, release_date, genre_id),
        )
        album_id = cursor.lastrowid

        # Insert songs in the album
        for song_title in song_titles:
            cursor.execute(
                """
                INSERT INTO Songs (song_title, artist_id, album_id, release_date)
                VALUES (%s, %s, %s, %s)
            """,
                (song_title, artist_id, album_id, release_date),
            )
            song_id = cursor.lastrowid

            # Link song to album's genre
            cursor.execute(
                """
                INSERT INTO SongGenres (song_id, genre_id)
                VALUES (%s, %s)
            """,
                (song_id, genre_id),
            )

    mydb.commit()
    cursor.close()
    return rejected


def get_top_song_genres(mydb, n: int) -> List[Tuple[str, int]]:
    """
    Get n genres that are most represented in terms of number of songs in that genre.
    Songs include singles as well as songs in albums.

    Args:
        mydb: database connection
        n: number of genres

    Returns:
        List[Tuple[str,int]]: list of tuples (genre,number_of_songs), from most represented to
        least represented genre. If number of genres is less than n, returns all.
        Ties broken by alphabetical order of genre names.
    """
    cursor = mydb.cursor()

    cursor.execute(
        """
        SELECT g.genre_name, COUNT(DISTINCT sg.song_id) as num_songs
        FROM Genres g
        JOIN SongGenres sg ON g.genre_id = sg.genre_id
        GROUP BY g.genre_id, g.genre_name
        ORDER BY num_songs DESC, g.genre_name ASC
        LIMIT %s
    """,
        (n,),
    )

    results = [(row[0], row[1]) for row in cursor.fetchall()]
    cursor.close()
    return results


def get_album_and_single_artists(mydb) -> Set[str]:
    """
    Get artists who have released albums as well as singles.

    Args:
        mydb; database connection

    Returns:
        Set[str]: set of artist names
    """
    cursor = mydb.cursor()

    cursor.execute(
        """
        SELECT DISTINCT a.artist_name
        FROM Artists a
        WHERE EXISTS (
            SELECT 1 FROM Songs s
            WHERE s.artist_id = a.artist_id AND s.album_id IS NULL
        )
        AND EXISTS (
            SELECT 1 FROM Songs s2
            WHERE s2.artist_id = a.artist_id AND s2.album_id IS NOT NULL
        )
    """
    )

    results = {row[0] for row in cursor.fetchall()}
    cursor.close()
    return results


def load_users(mydb, users: List[str]) -> Set[str]:
    """
    Add users to the database.

    Args:
        mydb: database connection
        users: list of usernames

    Returns:
        Set[str]: set of all usernames that were not added (rejected) because
        they are duplicates of existing users.
        Set is empty if there are no rejects.
    """
    cursor = mydb.cursor()
    rejected = set()

    for username in users:
        # Check if user already exists
        cursor.execute("SELECT user_id FROM Users WHERE user_name = %s", (username,))
        if cursor.fetchone():
            rejected.add(username)
        else:
            cursor.execute("INSERT INTO Users (user_name) VALUES (%s)", (username,))

    mydb.commit()
    cursor.close()
    return rejected


def load_song_ratings(
    mydb, song_ratings: List[Tuple[str, Tuple[str, str], int, str]]
) -> Set[Tuple[str, str, str]]:
    """
    Load ratings for songs, which are either singles or songs in albums.

    Args:
        mydb: database connection
        song_ratings: list of rating tuples of the form:
            (rater, (artist, song), rating, date)

        The rater is a username, the (artist,song) tuple refers to the uniquely identifiable song to be rated.
        e.g. ('u1',('a1','song1'),4,'2021-11-18') => u1 is giving a rating of 4 to the (a1,song1) song.

    Returns:
        Set[Tuple[str,str,str]]: set of (username,artist,song) tuples that are rejected, for any of the following
        reasongs:
        (a) username (rater) is not in the database, or
        (b) username is in database but (artist,song) combination is not in the database, or
        (c) username has already rated (artist,song) combination, or
        (d) everything else is legit, but rating is not in range 1..5

        An empty set is returned if there are no rejects.
    """
    cursor = mydb.cursor()
    rejected = set()

    for username, (artist_name, song_title), rating, rating_date in song_ratings:
        # Check rating is in valid range
        if rating < 1 or rating > 5:
            rejected.add((username, artist_name, song_title))
            continue

        # Check if user exists
        cursor.execute("SELECT user_id FROM Users WHERE user_name = %s", (username,))
        user_result = cursor.fetchone()
        if not user_result:
            rejected.add((username, artist_name, song_title))
            continue
        user_id = user_result[0]

        # Check if (artist, song) exists
        cursor.execute(
            """
            SELECT s.song_id FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            WHERE a.artist_name = %s AND s.song_title = %s
        """,
            (artist_name, song_title),
        )
        song_result = cursor.fetchone()
        if not song_result:
            rejected.add((username, artist_name, song_title))
            continue
        song_id = song_result[0]

        # Check if user has already rated this song
        cursor.execute(
            """
            SELECT rating_id FROM Ratings
            WHERE user_id = %s AND song_id = %s
        """,
            (user_id, song_id),
        )
        if cursor.fetchone():
            rejected.add((username, artist_name, song_title))
            continue

        # Insert the rating
        cursor.execute(
            """
            INSERT INTO Ratings (user_id, song_id, rating, rating_date)
            VALUES (%s, %s, %s, %s)
        """,
            (user_id, song_id, rating, rating_date),
        )

    mydb.commit()
    cursor.close()
    return rejected


def get_most_rated_songs(
    mydb, year_range: Tuple[int, int], n: int
) -> List[Tuple[str, str, int]]:
    """
    Get the top n most rated songs in the given year range (both inclusive),
    ranked from most rated to least rated.
    "Most rated" refers to number of ratings, not actual rating scores.
    Ties are broken in alphabetical order of song title. If the number of rated songs is less
    than n, all rates songs are returned.

    Args:
        mydb: database connection
        year_range: range of years, e.g. (2018-2021), during which ratings were given
        n: number of most rated songs

    Returns:
        List[Tuple[str,str,int]: list of (song title, artist name, number of ratings for song)
    """
    cursor = mydb.cursor()

    cursor.execute(
        """
        SELECT s.song_title, a.artist_name, COUNT(*) as num_ratings
        FROM Ratings r
        JOIN Songs s ON r.song_id = s.song_id
        JOIN Artists a ON s.artist_id = a.artist_id
        WHERE YEAR(r.rating_date) BETWEEN %s AND %s
        GROUP BY s.song_id, s.song_title, a.artist_name
        ORDER BY num_ratings DESC, s.song_title ASC
        LIMIT %s
    """,
        (year_range[0], year_range[1], n),
    )

    results = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
    cursor.close()
    return results


def get_most_engaged_users(
    mydb, year_range: Tuple[int, int], n: int
) -> List[Tuple[str, int]]:
    """
    Get the top n most engaged users, in terms of number of songs they have rated.
    Break ties by alphabetical order of usernames.

    Args:
        mydb: database connection
        year_range: range of years, e.g. (2018-2021), during which ratings were given
        n: number of users

    Returns:
        List[Tuple[str, int]]: list of (username,number_of_songs_rated) tuples
    """
    cursor = mydb.cursor()

    cursor.execute(
        """
        SELECT u.user_name, COUNT(*) as num_ratings
        FROM Ratings r
        JOIN Users u ON r.user_id = u.user_id
        WHERE YEAR(r.rating_date) BETWEEN %s AND %s
        GROUP BY u.user_id, u.user_name
        ORDER BY num_ratings DESC, u.user_name ASC
        LIMIT %s
    """,
        (year_range[0], year_range[1], n),
    )

    results = [(row[0], row[1]) for row in cursor.fetchall()]
    cursor.close()
    return results


def main():
    """
    Main function - example usage
    Update DB_CONFIG with your database credentials before running
    """
    import mysql.connector

    # Database configuration - UPDATE THESE VALUES
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "root",  # Change this
        "database": "musicdb",  # Change this
    }
    print("Music Database Management System")
    print("=" * 50)
    print("Update DB_CONFIG in the main() function before running.")
    print("See test_music_db.py for comprehensive test suite.")
    print("See example_usage.py for simple usage examples.")
    print("See README.md for setup instructions.")


if __name__ == "__main__":
    main()
