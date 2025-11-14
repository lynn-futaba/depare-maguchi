CREATE DATABASE IF NOT EXISTS depal;
USE depal;

-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
-- Host: localhost    Database: depal
-- ------------------------------------------------------
-- Server version 8.0.41

DROP TABLE IF EXISTS `depallet_frontage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `depallet_frontage` (
  `frontage_id` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `cell_code` varchar(8) NOT NULL,
  `priority` int NOT NULL,
  PRIMARY KEY (`frontage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `depallet_frontage`
--
/*!40000 ALTER TABLE `depallet_frontage` DISABLE KEYS */;
INSERT INTO `depallet_frontage` VALUES (1,'間口1','1',4),(2,'間口2','2',2),(3,'間口3','3',1),(4,'間口4','4',3),(5,'間口5','5',5);
