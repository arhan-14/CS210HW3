-- MySQL dump 10.13  Distrib 8.4.7, for Linux (x86_64)
--
-- Host: localhost    Database: musicdb
-- ------------------------------------------------------
-- Server version	8.4.7

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Albums`
--

DROP TABLE IF EXISTS `Albums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Albums` (
  `album_id` smallint NOT NULL AUTO_INCREMENT,
  `album_name` varchar(100) NOT NULL,
  `artist_id` smallint NOT NULL,
  `release_date` date NOT NULL,
  `genre_id` smallint NOT NULL,
  PRIMARY KEY (`album_id`),
  UNIQUE KEY `album_name` (`album_name`,`artist_id`),
  KEY `artist_id` (`artist_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `Albums_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`artist_id`),
  CONSTRAINT `Albums_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `Genres` (`genre_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Albums`
--

LOCK TABLES `Albums` WRITE;
/*!40000 ALTER TABLE `Albums` DISABLE KEYS */;
INSERT INTO `Albums` VALUES (13,'25',43,'2015-11-20',31),(14,'Thriller Album',39,'1982-11-30',31),(15,'Fine Line',50,'2019-12-13',31),(16,'Abbey Road',48,'1969-09-26',33),(17,'Dark Side of the Moon',51,'1973-03-01',45),(18,'Back in Black',52,'1980-07-25',33);
/*!40000 ALTER TABLE `Albums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Artists`
--

DROP TABLE IF EXISTS `Artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artists` (
  `artist_id` smallint NOT NULL AUTO_INCREMENT,
  `artist_name` varchar(120) NOT NULL,
  PRIMARY KEY (`artist_id`),
  UNIQUE KEY `artist_name` (`artist_name`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Artists`
--

LOCK TABLES `Artists` WRITE;
/*!40000 ALTER TABLE `Artists` DISABLE KEYS */;
INSERT INTO `Artists` VALUES (52,'AC/DC'),(43,'Adele'),(49,'Billie Eilish'),(40,'Eagles'),(37,'Ed Sheeran'),(44,'Eminem'),(45,'Guns N Roses'),(50,'Harry Styles'),(42,'John Lennon'),(47,'Led Zeppelin'),(39,'Michael Jackson'),(41,'Nirvana'),(46,'Oasis'),(51,'Pink Floyd'),(38,'Queen'),(48,'The Beatles'),(36,'The Weeknd');
/*!40000 ALTER TABLE `Artists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Genres`
--

DROP TABLE IF EXISTS `Genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Genres` (
  `genre_id` smallint NOT NULL AUTO_INCREMENT,
  `genre_name` varchar(60) NOT NULL,
  PRIMARY KEY (`genre_id`),
  UNIQUE KEY `genre_name` (`genre_name`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Genres`
--

LOCK TABLES `Genres` WRITE;
/*!40000 ALTER TABLE `Genres` DISABLE KEYS */;
INSERT INTO `Genres` VALUES (44,'Alternative'),(40,'Britpop'),(43,'Electropop'),(41,'Funk'),(36,'Grunge'),(38,'Hip Hop'),(42,'Jazz'),(34,'Opera'),(31,'Pop'),(45,'Progressive Rock'),(35,'R&B'),(39,'Rap'),(33,'Rock'),(37,'Soul'),(32,'Synth-pop');
/*!40000 ALTER TABLE `Genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ratings`
--

DROP TABLE IF EXISTS `Ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ratings` (
  `rating_id` smallint NOT NULL AUTO_INCREMENT,
  `user_id` smallint NOT NULL,
  `song_id` smallint NOT NULL,
  `rating` tinyint NOT NULL,
  `rating_date` date NOT NULL,
  PRIMARY KEY (`rating_id`),
  UNIQUE KEY `user_id` (`user_id`,`song_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `Ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`),
  CONSTRAINT `Ratings_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `Songs` (`song_id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ratings`
--

LOCK TABLES `Ratings` WRITE;
/*!40000 ALTER TABLE `Ratings` DISABLE KEYS */;
INSERT INTO `Ratings` VALUES (49,27,110,5,'2020-01-15'),(50,27,111,4,'2020-02-10'),(51,27,117,5,'2020-03-20'),(52,28,112,5,'2020-01-20'),(53,28,115,5,'2020-02-15'),(54,28,122,5,'2020-03-10'),(55,29,110,4,'2020-01-25'),(56,29,113,5,'2020-02-20'),(57,30,133,5,'2020-04-01'),(58,30,134,4,'2020-04-02'),(59,31,130,4,'2021-01-15'),(60,31,126,5,'2021-02-10'),(61,32,124,5,'2021-03-05'),(62,33,121,5,'2021-04-12'),(63,34,118,5,'2021-05-18'),(64,35,123,4,'2021-06-22'),(65,36,114,5,'2021-07-30'),(66,28,110,4,'2020-06-15'),(67,29,117,4,'2020-07-20'),(68,30,110,5,'2020-08-25'),(69,31,112,5,'2020-09-30'),(70,32,110,5,'2020-10-15'),(71,33,111,4,'2020-11-20'),(72,34,110,4,'2020-12-25');
/*!40000 ALTER TABLE `Ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SongGenres`
--

DROP TABLE IF EXISTS `SongGenres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SongGenres` (
  `song_id` smallint NOT NULL,
  `genre_id` smallint NOT NULL,
  UNIQUE KEY `song_id` (`song_id`,`genre_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `SongGenres_ibfk_1` FOREIGN KEY (`song_id`) REFERENCES `Songs` (`song_id`),
  CONSTRAINT `SongGenres_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `Genres` (`genre_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SongGenres`
--

LOCK TABLES `SongGenres` WRITE;
/*!40000 ALTER TABLE `SongGenres` DISABLE KEYS */;
INSERT INTO `SongGenres` VALUES (110,31),(111,31),(113,31),(116,31),(117,31),(121,31),(123,31),(124,31),(126,31),(128,31),(129,31),(130,31),(131,31),(132,31),(133,31),(134,31),(135,31),(136,31),(137,31),(138,31),(139,31),(140,31),(141,31),(142,31),(143,31),(144,31),(145,31),(146,31),(147,31),(110,32),(112,33),(114,33),(115,33),(116,33),(119,33),(120,33),(122,33),(124,33),(130,33),(148,33),(149,33),(150,33),(151,33),(152,33),(158,33),(159,33),(160,33),(161,33),(162,33),(112,34),(113,35),(115,36),(117,37),(121,37),(118,38),(118,39),(120,40),(123,41),(125,42),(126,43),(127,44),(153,45),(154,45),(155,45),(156,45),(157,45);
/*!40000 ALTER TABLE `SongGenres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Songs`
--

DROP TABLE IF EXISTS `Songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Songs` (
  `song_id` smallint NOT NULL AUTO_INCREMENT,
  `song_title` varchar(100) NOT NULL,
  `artist_id` smallint NOT NULL,
  `album_id` smallint DEFAULT NULL,
  `release_date` date NOT NULL,
  PRIMARY KEY (`song_id`),
  UNIQUE KEY `song_title` (`song_title`,`artist_id`),
  KEY `artist_id` (`artist_id`),
  KEY `album_id` (`album_id`),
  CONSTRAINT `Songs_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`artist_id`),
  CONSTRAINT `Songs_ibfk_2` FOREIGN KEY (`album_id`) REFERENCES `Albums` (`album_id`)
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Songs`
--

LOCK TABLES `Songs` WRITE;
/*!40000 ALTER TABLE `Songs` DISABLE KEYS */;
INSERT INTO `Songs` VALUES (110,'Blinding Lights',36,NULL,'2019-11-29'),(111,'Shape of You',37,NULL,'2017-01-06'),(112,'Bohemian Rhapsody',38,NULL,'1975-10-31'),(113,'Billie Jean',39,NULL,'1983-01-02'),(114,'Hotel California',40,NULL,'1977-02-22'),(115,'Smells Like Teen Spirit',41,NULL,'1991-09-10'),(116,'Imagine',42,NULL,'1971-10-11'),(117,'Rolling in the Deep',43,NULL,'2010-11-29'),(118,'Lose Yourself',44,NULL,'2002-10-28'),(119,'Sweet Child O Mine',45,NULL,'1987-08-17'),(120,'Wonderwall',46,NULL,'1995-10-30'),(121,'Someone Like You',43,NULL,'2011-01-24'),(122,'Stairway to Heaven',47,NULL,'1971-11-08'),(123,'Thriller',39,NULL,'1984-01-23'),(124,'Hey Jude',48,NULL,'1968-08-26'),(125,'New Song',36,NULL,'2020-05-15'),(126,'Bad Guy',49,NULL,'2019-03-29'),(127,'Everything I Wanted',49,NULL,'2019-11-13'),(128,'Therefore I Am',49,NULL,'2020-11-12'),(129,'Happier Than Ever',49,NULL,'2021-07-30'),(130,'Watermelon Sugar',50,NULL,'2019-11-16'),(131,'Golden',50,NULL,'2019-10-26'),(132,'Adore You',50,NULL,'2019-12-06'),(133,'Hello',43,13,'2015-11-20'),(134,'Send My Love',43,13,'2015-11-20'),(135,'When We Were Young',43,13,'2015-11-20'),(136,'Remedy',43,13,'2015-11-20'),(137,'Water Under the Bridge',43,13,'2015-11-20'),(138,'Wanna Be Startin Somethin',39,14,'1982-11-30'),(139,'Baby Be Mine',39,14,'1982-11-30'),(140,'The Girl Is Mine',39,14,'1982-11-30'),(141,'Thriller Song',39,14,'1982-11-30'),(142,'Beat It',39,14,'1982-11-30'),(143,'Golden Album',50,15,'2019-12-13'),(144,'Watermelon Sugar Album',50,15,'2019-12-13'),(145,'Adore You Album',50,15,'2019-12-13'),(146,'Lights Up',50,15,'2019-12-13'),(147,'Cherry',50,15,'2019-12-13'),(148,'Come Together',48,16,'1969-09-26'),(149,'Something',48,16,'1969-09-26'),(150,'Maxwell Silver Hammer',48,16,'1969-09-26'),(151,'Oh Darling',48,16,'1969-09-26'),(152,'Octopus Garden',48,16,'1969-09-26'),(153,'Speak to Me',51,17,'1973-03-01'),(154,'Breathe',51,17,'1973-03-01'),(155,'On the Run',51,17,'1973-03-01'),(156,'Time',51,17,'1973-03-01'),(157,'Money',51,17,'1973-03-01'),(158,'Hells Bells',52,18,'1980-07-25'),(159,'Shoot to Thrill',52,18,'1980-07-25'),(160,'What Do You Do for Money Honey',52,18,'1980-07-25'),(161,'Given the Dog a Bone',52,18,'1980-07-25'),(162,'Let Me Put My Love into You',52,18,'1980-07-25');
/*!40000 ALTER TABLE `Songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `user_id` smallint NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (27,'alice_music'),(28,'bob_rocks'),(29,'charlie_pop'),(30,'diana_jazz'),(31,'eve_listener'),(32,'frank_fan'),(33,'grace_melody'),(34,'henry_beats'),(35,'iris_song'),(36,'jack_tunes'),(37,'new_user');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-09 17:52:59
