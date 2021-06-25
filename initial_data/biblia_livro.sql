-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: django_cadastro_perguntas
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `biblia_livro`
--

DROP TABLE IF EXISTS `biblia_livro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblia_livro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `posicao` int NOT NULL,
  `nome` varchar(20) NOT NULL,
  `testamento_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `biblia_livro_testamento_id_2dbf5a66_fk_biblia_testamento_id` (`testamento_id`),
  CONSTRAINT `biblia_livro_testamento_id_2dbf5a66_fk_biblia_testamento_id` FOREIGN KEY (`testamento_id`) REFERENCES `biblia_testamento` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblia_livro`
--

LOCK TABLES `biblia_livro` WRITE;
/*!40000 ALTER TABLE `biblia_livro` DISABLE KEYS */;
INSERT INTO `biblia_livro` VALUES (1,1,'Genesis',1),(2,2,'Exodo',1),(3,3,'Levitico',1),(4,4,'Numeros',1),(5,5,'Deuteronomio',1),(6,6,'Josue',1),(7,7,'Juizes',1),(8,8,'Rute',1),(9,9,'I Samuel',1),(10,10,'II Samuel',1),(11,11,'I Reis',1),(12,12,'II Reis',1),(13,13,'I Cronicas',1),(14,14,'II Cronicas',1),(15,15,'Esdras',1),(16,16,'Neemias',1),(17,17,'Ester',1),(18,18,'Jo',1),(19,19,'Salmos',1),(20,20,'Proverbios',1),(21,21,'Eclesiastes',1),(22,22,'Cantico dos Canticos',1),(23,23,'Isaias',1),(24,24,'Jeremias',1),(25,25,'Lamentacoes Jeremias',1),(26,26,'Ezequiel',1),(27,27,'Daniel',1),(28,28,'Oseias',1),(29,29,'Joel',1),(30,30,'Amos',1),(31,31,'Obadias',1),(32,32,'Jonas',1),(33,33,'Miqueias',1),(34,34,'Naum',1),(35,35,'Habacuque',1),(36,36,'Sofonias',1),(37,37,'Ageu',1),(38,38,'Zacarias',1),(39,39,'Malaquias',1),(40,1,'Mateus',2),(41,2,'Marcos',2),(42,3,'Lucas',2),(43,4,'Joao',2),(44,5,'Atos',2),(45,6,'Romanos',2),(46,7,'I Corintios',2),(47,8,'II Corintios',2),(48,9,'Galatas',2),(49,10,'Efesios',2),(50,11,'Filipenses',2),(51,12,'Colossenses',2),(52,13,'I Tessalonicenses',2),(53,14,'II Tessalonicenses',2),(54,15,'I Timoteo',2),(55,16,'II Timoteo',2),(56,17,'Tito',2),(57,18,'Filemom',2),(58,19,'Hebreus',2),(59,20,'Tiago',2),(60,21,'I Pedro',2),(61,22,'II Pedro',2),(62,23,'I Joao',2),(63,24,'II Joao',2),(64,25,'III Joao',2),(65,26,'Judas',2),(66,27,'Apocalipse',2);
/*!40000 ALTER TABLE `biblia_livro` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-25  3:21:09
