CREATE TABLE Artists (
    artist_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE Genres (
    genre_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE Users (
    user_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Albums (
    album_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    album_name VARCHAR(100) NOT NULL,
    artist_id SMALLINT NOT NULL,
    release_date DATE NOT NULL,
    genre_id SMALLINT NOT NULL,
    UNIQUE (album_name, artist_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id),
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);

CREATE TABLE Songs (
    song_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    song_title VARCHAR(100) NOT NULL,
    artist_id SMALLINT NOT NULL,
    album_id SMALLINT NULL,
    release_date DATE NOT NULL,
    UNIQUE (song_title, artist_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id),
    FOREIGN KEY (album_id) REFERENCES Albums(album_id)
);

CREATE TABLE SongGenres (
    song_id SMALLINT NOT NULL,
    genre_id SMALLINT NOT NULL,
    UNIQUE (song_id, genre_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id),
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);

CREATE TABLE Ratings (
    rating_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    user_id SMALLINT NOT NULL,
    song_id SMALLINT NOT NULL,
    rating TINYINT NOT NULL,
    rating_date DATE NOT NULL,
    UNIQUE (user_id, song_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);