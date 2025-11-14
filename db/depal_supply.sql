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
-- Table structure for table `supply`
--

DROP TABLE IF EXISTS `supply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supply` (
  `inventory_id` int NOT NULL,
  `time_stamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `quantity` int NOT NULL,
  PRIMARY KEY (`inventory_id`,`time_stamp`),
  KEY `line_inventory_idx` (`inventory_id`),
  CONSTRAINT `line_inventory` FOREIGN KEY (`inventory_id`) REFERENCES `line_inventory` (`inventory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supply`
--

LOCK TABLES `supply` WRITE;
/*!40000 ALTER TABLE `supply` DISABLE KEYS */;
INSERT INTO `supply` VALUES (1,'2025-09-01 00:00:00',4),(1,'2025-09-26 15:57:20',2),(1,'2025-09-26 16:02:50',5),(1,'2025-09-26 16:34:43',5),(1,'2025-09-26 16:35:06',5),(1,'2025-09-26 16:35:51',5),(1,'2025-09-26 16:37:25',5),(1,'2025-09-26 16:38:36',5),(1,'2025-09-26 16:40:55',5),(1,'2025-09-26 16:42:49',5),(1,'2025-09-26 16:57:24',5),(1,'2025-10-13 16:03:27',10),(1,'2025-10-24 00:00:00',1),(1,'2025-10-24 00:10:00',10),(1,'2025-10-24 13:48:42',2),(1,'2025-10-30 14:20:54',1),(1,'2025-10-30 14:22:01',1),(1,'2025-10-30 14:23:59',1),(1,'2025-10-30 14:25:15',1),(1,'2025-10-30 14:29:17',1),(1,'2025-10-30 14:34:57',1),(1,'2025-10-30 14:36:10',1),(1,'2025-10-30 14:37:05',1),(1,'2025-10-30 14:39:27',1),(1,'2025-10-30 14:43:31',1),(1,'2025-11-06 12:58:16',1),(1,'2025-11-06 13:10:04',1),(1,'2025-11-06 13:18:09',1),(1,'2025-11-06 13:19:26',1),(1,'2025-11-06 13:20:43',1),(1,'2025-11-06 13:23:15',1),(1,'2025-11-06 16:33:42',1),(2,'2025-09-01 00:00:00',4),(2,'2025-10-13 16:03:27',2),(2,'2025-10-24 00:00:00',4),(2,'2025-10-24 00:10:00',10),(2,'2025-10-24 13:48:42',2),(3,'2025-09-01 00:00:00',4),(3,'2025-10-24 00:00:00',4),(3,'2025-10-24 00:10:00',10),(4,'2025-09-01 00:00:00',4),(4,'2025-10-24 00:00:00',4),(4,'2025-10-24 00:10:00',10),(5,'2025-09-01 00:00:00',4),(5,'2025-10-24 00:00:00',4),(5,'2025-10-24 00:10:00',10),(6,'2025-09-01 00:00:00',4),(6,'2025-10-24 00:00:00',4),(6,'2025-10-24 00:10:00',10),(7,'2025-09-01 00:00:00',4),(7,'2025-10-24 00:00:00',4),(7,'2025-10-24 00:10:00',10),(8,'2025-09-01 00:00:00',4),(8,'2025-10-24 00:00:00',4),(8,'2025-10-24 00:10:00',10),(9,'2025-09-01 00:00:00',4),(9,'2025-10-24 00:00:00',4),(9,'2025-10-24 00:10:00',10),(10,'2025-09-01 00:00:00',4),(10,'2025-10-24 00:00:00',4),(10,'2025-10-24 00:10:00',10);
/*!40000 ALTER TABLE `supply` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `supply_AFTER_INSERT` AFTER INSERT ON `supply` FOR EACH ROW BEGIN

DECLARE number INT default 0;

SELECT max(depal.m_product_inventory.innner_parts) into number FROM depal.line_inventory
inner join depal.m_product using(part_number)
inner join depal.m_product_inventory using(part_number)
where inventory_id=new.inventory_id;

update depal.line_inventory 
set case_quantity=(case_quantity+new.quantity) ,part_quantity=(part_quantity+number*new.quantity),update_date=new.time_stamp
where depal.line_inventory.inventory_id = new.inventory_id;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 12:58:36
