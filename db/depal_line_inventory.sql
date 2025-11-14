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
-- Table structure for table `line_inventory`
--

DROP TABLE IF EXISTS `line_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `line_inventory` (
  `inventory_id` int NOT NULL,
  `frontage_id` int NOT NULL,
  `part_number` varchar(20) NOT NULL,
  `case_quantity` int NOT NULL,
  `part_quantity` int NOT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`inventory_id`),
  KEY `frontage_idx` (`frontage_id`),
  KEY `part_idx` (`part_number`),
  CONSTRAINT `frontage` FOREIGN KEY (`frontage_id`) REFERENCES `line_frontage` (`frontage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `line_inventory`
--

LOCK TABLES `line_inventory` WRITE;
/*!40000 ALTER TABLE `line_inventory` DISABLE KEYS */;
INSERT INTO `line_inventory` VALUES (1,1,'1001-0001',29,284,'2025-11-06 16:33:42'),(2,1,'1001-0002',9,18,'2025-10-28 14:34:26'),(3,2,'1002-0001',4,4,'2025-10-28 14:34:26'),(4,3,'1002-0002',4,4,'2025-10-28 14:34:26'),(5,3,'1003-0001',4,4,'2025-10-28 14:34:26'),(6,4,'1004-0001',10,10,'2025-10-24 00:10:00'),(7,4,'1005-0001',10,10,'2025-10-24 00:10:00'),(8,5,'1006-0001',10,10,'2025-10-24 00:10:00'),(9,5,'1007-0001',10,10,'2025-10-24 00:10:00'),(10,6,'1008-0001',10,10,'2025-10-24 00:10:00');
/*!40000 ALTER TABLE `line_inventory` ENABLE KEYS */;
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
