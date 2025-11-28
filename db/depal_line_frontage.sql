-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: depal
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `line_frontage`
--

DROP TABLE IF EXISTS `line_frontage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `line_frontage` (
  `frontage_id` int NOT NULL,
  `line_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `cell_code` varchar(8) NOT NULL,
  `car_model_id` int NOT NULL,
  PRIMARY KEY (`frontage_id`),
  KEY `line_idx` (`line_id`),
  KEY `line_99_idx` (`line_id`),
  CONSTRAINT `line_99` FOREIGN KEY (`line_id`) REFERENCES `line` (`line_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `line_frontage`
--

LOCK TABLES `line_frontage` WRITE;
/*!40000 ALTER TABLE `line_frontage` DISABLE KEYS */;
INSERT INTO `line_frontage` VALUES (1,1,'供給間口R1','6',201),(2,1,'供給間口R2','7',202),(3,1,'供給間口R3','8',203),(4,2,'供給間口L1','9',204),(5,2,'供給間口L2','10',205),(6,2,'供給間口L3','11',206),(7,3,'供給間口R1','12',207),(8,3,'供給間口R2','13',208),(9,3,'供給間口R3','14',209),(10,4,'供給間口L1','15',210),(11,4,'供給間口L2','16',211),(12,4,'供給間口L3','17',212);
/*!40000 ALTER TABLE `line_frontage` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 12:58:34
