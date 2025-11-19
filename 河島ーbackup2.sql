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
-- Table structure for table `composition`
--

DROP TABLE IF EXISTS `composition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `composition` (
  `product_id` varchar(20) NOT NULL,
  `part_number` varchar(20) NOT NULL,
  `quantity` varchar(45) NOT NULL,
  PRIMARY KEY (`product_id`,`part_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `composition`
--

LOCK TABLES `composition` WRITE;
/*!40000 ALTER TABLE `composition` DISABLE KEYS */;
INSERT INTO `composition` VALUES ('1111-1111','1001-0001','2'),('1111-1111','1001-0002','2'),('1111-1111','1002-0001','2'),('1111-1111','1002-0002','2'),('1111-1111','1003-0001','2'),('1111-1111','1003-0002','2'),('1111-1112','1004-0001','2'),('1111-1112','1004-0002','2'),('1111-1112','1005-0001','2'),('1111-1112','1005-0002','2');
/*!40000 ALTER TABLE `composition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `depallet_area`
--

DROP TABLE IF EXISTS `depallet_area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `depallet_area` (
  `area_id` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`area_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `depallet_area`
--

LOCK TABLES `depallet_area` WRITE;
/*!40000 ALTER TABLE `depallet_area` DISABLE KEYS */;
INSERT INTO `depallet_area` VALUES (1,'A'),(2,'B');
/*!40000 ALTER TABLE `depallet_area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `depallet_frontage`
--

DROP TABLE IF EXISTS `depallet_frontage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `depallet_frontage` (
  `frontage_id` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `cell_code` varchar(8) NOT NULL,
  `priority` int NOT NULL,
  PRIMARY KEY (`frontage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `depallet_frontage`
--

LOCK TABLES `depallet_frontage` WRITE;
/*!40000 ALTER TABLE `depallet_frontage` DISABLE KEYS */;
INSERT INTO `depallet_frontage` VALUES (1,'間口1','1',4),(2,'間口2','2',2),(3,'間口3','3',1),(4,'間口4','4',3),(5,'間口5','5',5);
/*!40000 ALTER TABLE `depallet_frontage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `futaba_product`
--

DROP TABLE IF EXISTS `futaba_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `futaba_product` (
  `product_id` varchar(20) NOT NULL,
  `kanban_no` varchar(10) NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `futaba_product`
--

LOCK TABLES `futaba_product` WRITE;
/*!40000 ALTER TABLE `futaba_product` DISABLE KEYS */;
INSERT INTO `futaba_product` VALUES ('1111-1111','1111','product_R'),('1111-1112','2222','product_L'),('2222-1111','3333','product_R'),('2222-1112','4444','product_L');
/*!40000 ALTER TABLE `futaba_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `line`
--

DROP TABLE IF EXISTS `line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `line` (
  `line_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `process` varchar(10) NOT NULL,
  PRIMARY KEY (`line_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `line`
--

LOCK TABLES `line` WRITE;
/*!40000 ALTER TABLE `line` DISABLE KEYS */;
INSERT INTO `line` VALUES (1,'Aライン','R'),(2,'Aライン','L'),(3,'Bライン','R'),(4,'Bライン','L');
/*!40000 ALTER TABLE `line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `line_depallet_frontage`
--

DROP TABLE IF EXISTS `line_depallet_frontage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `line_depallet_frontage` (
  `line_id` int NOT NULL,
  `frontage_id` int NOT NULL,
  PRIMARY KEY (`line_id`,`frontage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `line_depallet_frontage`
--

LOCK TABLES `line_depallet_frontage` WRITE;
/*!40000 ALTER TABLE `line_depallet_frontage` DISABLE KEYS */;
INSERT INTO `line_depallet_frontage` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,2),(2,3),(2,4),(2,5);
/*!40000 ALTER TABLE `line_depallet_frontage` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `line_frontage` VALUES (1,1,'供給間口R1','6',201),(2,1,'供給間口R2','7',202),(3,1,'供給間口R3','8',203),(4,2,'供給間口L1','9',204),(5,2,'供給間口L2','10',205),(6,2,'供給間口L3','11',206),(7,3,'供給間口R1','12',207),(8,3,'供給間口R2','13',208),(9,3,'供給間口R3','14',209),(10,4,'供給間口R1','15',210),(11,4,'供給間口L2','16',211),(12,4,'供給間口L3','17',212);
/*!40000 ALTER TABLE `line_frontage` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Table structure for table `line_product`
--

DROP TABLE IF EXISTS `line_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `line_product` (
  `line_id` int NOT NULL,
  `product_id` varchar(20) NOT NULL,
  PRIMARY KEY (`line_id`,`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `line_product`
--

LOCK TABLES `line_product` WRITE;
/*!40000 ALTER TABLE `line_product` DISABLE KEYS */;
INSERT INTO `line_product` VALUES (1,'1111-1111'),(2,'1111-1112'),(3,'2222-1111'),(4,'2222-1112');
/*!40000 ALTER TABLE `line_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `m_product`
--

DROP TABLE IF EXISTS `m_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_product` (
  `part_number` varchar(20) NOT NULL,
  `kanban_no` text,
  `box_code` text,
  `pallet_type` text,
  `kotatsu_type` text,
  `dock` text,
  `route_cd` text,
  `supplier_cd` text,
  `supplier_name` text,
  `dest_process` text,
  `dest_plat` int DEFAULT NULL,
  `rotate_angle` int DEFAULT NULL,
  `rotate_direction` int DEFAULT NULL,
  `status_color` text,
  `load_capacity` int DEFAULT NULL,
  `car_model_id` int DEFAULT NULL,
  `create_datetime` text,
  `update_datetime` text,
  PRIMARY KEY (`part_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_product`
--

LOCK TABLES `m_product` WRITE;
/*!40000 ALTER TABLE `m_product` DISABLE KEYS */;
INSERT INTO `m_product` VALUES ('000000000ALa','FLOWa','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',81,0,0,'fafaaa',0,201,'2025/10/17 9:25:05','2025/10/21 11:30:05'),('000000000ALb','FLOWb','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',82,0,0,'fafaaa',0,202,'2025/10/17 9:25:05','2025/10/21 11:30:09'),('000000000ALc','FLOWc','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',83,0,0,'fafaaa',0,203,'2025/10/17 9:25:05','2025/10/21 11:30:11'),('000000000ARa','FLOWa','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',74,0,0,'fafaaa',0,204,'2025/10/17 9:25:05','2025/10/21 11:30:12'),('000000000ARb','FLOWb','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',75,0,0,'fafaaa',0,205,'2025/10/17 9:25:05','2025/10/21 11:30:15'),('000000000ARc','FLOWc','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',76,0,0,'fafaaa',0,206,'2025/10/17 9:25:05','2025/10/21 11:30:17'),('000000000BLa','FLOWa','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',101,0,0,'fafaaa',0,201,'2025/10/17 9:25:05','2025/10/21 11:30:22'),('000000000BLb','FLOWb','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',102,0,0,'fafaaa',0,202,'2025/10/17 9:25:05','2025/10/21 11:30:24'),('000000000BLc','FLOWc','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',103,0,0,'fafaaa',0,203,'2025/10/17 9:25:05','2025/10/21 11:30:25'),('000000000BRa','FLOWa','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',94,0,0,'fafaaa',0,204,'2025/10/17 9:25:05','2025/10/21 11:30:26'),('000000000BRb','FLOWb','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',95,0,0,'fafaaa',0,205,'2025/10/17 9:25:05','2025/10/21 11:30:28'),('000000000BRc','FLOWc','FLOWrack','C','C','B','-','suppl','工程内搬送用','store2',96,0,0,'fafaaa',0,206,'2025/10/17 9:25:05','2025/10/21 11:30:32'),('1001-0001','101','LH1','D','D','LH45','routeLift1','suppl','テスト用A','store2',45,0,0,'fafacc',10,1,'2024/10/07 7:08:00','2025/10/21 11:21:21'),('1001-0002','102','RH1','D','D','RH58','routeLift1','suppl','テスト用B','store2',58,0,0,'fafacc',2,2,'2024/10/07 7:08:00','2025/10/21 11:21:26'),('1002-0001','201','P','C','C','RH1','routeLift1','suppl','テスト用A','store2',60,0,0,'fafacc',1,3,'2024/10/07 7:08:00','2025/10/21 11:21:28'),('1002-0002','202','P','C','C','LH1','routeLift1','suppl','テスト用B','store2',60,0,0,'fafacc',1,4,'2024/10/07 7:08:00','2025/10/21 11:21:30'),('1003-0001','301','RH/A','A','A','RH55','routeLift1','suppl','テスト用A','store2',55,0,0,'fafacc',1,5,'2024/10/07 7:08:00','2025/10/21 11:21:33'),('1004-0001','401','RH/B','A','A','RH57','routeLift1','suppl','テスト用A','store2',57,0,0,'fafacc',1,6,'2024/10/07 7:08:00','2025/10/21 11:21:38'),('1005-0001','501','LH/A','A','A','LH43','routeLift1','suppl','テスト用A','store2',43,0,0,'fafacc',1,7,'2024/10/07 7:08:00','2025/10/21 11:21:40'),('1006-0001','601','LH/B','A','A','LH44','routeLift2','suppl','テスト用F','store2',44,0,0,'fafacc',1,8,'2024/10/07 7:08:00','2025/10/21 11:21:43'),('1006-0002','602','P','C','C','RH4','routeLift2','suppl','テスト用F','store2',60,0,0,'fafacc',1,9,'2024/10/07 7:08:00','2025/10/21 11:21:48'),('1006-0003','603','P','C','C','RH4','routeLift2','suppl','テスト用F2','store2',60,0,0,'fafacc',1,10,'2024/10/07 7:08:00','2025/10/21 11:21:52'),('1007-0001','701','P','C','C','LH4','routeLiftS','suppl','テスト用G','store2',60,0,0,'fafacc',1,11,'2024/10/07 7:08:00','2025/10/21 11:21:54'),('1008-0001','801','P','C','C','LH4','routeLiftS','suppl','テスト用H','store2',60,0,0,'fafacc',1,12,'2024/10/07 7:08:00','2025/10/21 11:21:56'),('1009-0001','901','RH/A1/2','A','A','RH52','-','suppl','テスト用K','store2',52,0,0,'fafacc',1,13,'2024/10/07 7:08:00','2025/10/21 11:21:59'),('1010-0001','1010','LH/A1/2','A','A','LH41','routeLift1','suppl','テスト用C','store2',41,0,0,'fafacc',1,14,'2024/10/07 7:08:00','2025/10/21 11:22:02'),('1011-0001','1011','RH/B','A','A','RH54','-','suppl','テスト用R','store2',54,0,0,'fafacc',1,15,'2024/10/07 7:08:00','2025/10/21 11:22:07'),('57413-42090','3190','A','A','A','A','routeLift1','suppl','緑工','store2',62,0,0,'fafacc',200,101,'2025/10/16 13:38:00','2025/10/16 15:35:09'),('57413-42100-','3192','A','A','A','A','routeLift2','suppl','緑工‐NUT','store2',54,0,0,'fafacc',200,102,'2025/10/16 13:39:00','2025/10/16 15:08:00'),('57414-42090','3200','A','A','A','A','routeLift1','suppl','緑工','store2',54,0,0,'fafacc',200,103,'2025/10/16 14:55:00','2025/10/16 15:08:00'),('57414-42100','3202','A','A','A','A','routeLift2','suppl','緑工‐NUT','store2',54,0,0,'fafacc',200,104,'2025/10/16 14:56:00','2025/10/16 15:08:00'),('57415-42040','ｱ618','TP332','D','D','D','routeLift1','suppl','浅井製作所','store2',54,0,0,'fafacc',100,105,'2025/10/16 13:38:00','2025/10/16 15:08:00'),('57416-42030','ｱ619','TP332','D','D','D','routeLift1','suppl','浅井製作所','store2',54,0,0,'fafacc',100,106,'2025/10/16 14:58:00','2025/10/16 15:08:00'),('57435-42010','T435','TP341','D','D','D','routeLift1','suppl','豊鉄額田','store2',54,0,0,'fafacc',30,107,'2025/10/16 13:40:00','2025/10/16 15:08:00'),('57436-42010','T436','TP341','D','D','D','routeLift1','suppl','豊鉄額田','store2',54,0,0,'fafacc',30,108,'2025/10/16 14:57:00','2025/10/16 15:08:00'),('57607-42090','ｻ607','TP332','D','D','D','routeLift1','suppl','三五','store2',54,0,0,'fafacc',18,109,'2025/10/16 13:21:00','2025/10/16 15:08:00'),('57611-42070-','5121','A','A','A','A','routeLift1','suppl','幸工','store2',54,0,0,'fafacc',70,110,'2025/10/16 13:24:00','2025/10/16 15:08:00'),('57612-42070-','5131','A','A','A','A','routeLift1','suppl','幸工','store2',54,0,0,'fafacc',70,111,'2025/10/16 13:42:00','2025/10/16 15:08:00'),('57621-42010','T621','TP332','D','D','D','routeLift1','suppl','豊鉄額田','store2',54,0,0,'fafacc',40,112,'2025/10/16 13:32:00','2025/10/16 15:08:00'),('57622-42010','T622','TP321','D','D','D','routeLift1','suppl','豊鉄額田','store2',54,0,0,'fafacc',40,113,'2025/10/16 14:14:00','2025/10/16 15:08:00'),('57631-42020','T631','TP332','D','D','D','routeLift1','suppl','豊鉄細谷','store2',54,0,0,'fafacc',16,114,'2025/10/16 13:33:00','2025/10/16 15:08:00'),('57632-42060','T632','TP332','D','D','D','routeLift1','suppl','豊鉄細谷','store2',54,0,0,'fafacc',16,115,'2025/10/16 14:41:00','2025/10/16 14:41:00'),('57637-42070','3237','TP342','D','D','D','routeLift1','suppl','緑工','store2',54,0,0,'fafacc',40,116,'2025/10/16 13:34:00','2025/10/16 13:34:00'),('57638-42050','3238','TP342','D','D','D','routeLift1','suppl','緑工','store2',54,0,0,'fafacc',40,117,'2025/10/16 14:42:00','2025/10/16 14:42:00'),('57641-42030','ﾀ032','TP332','D','D','D','routeLift1','suppl','高木製作所','store2',54,0,0,'fafacc',50,118,'2025/10/16 13:36:00','2025/10/16 13:36:00'),('57642-42030','ﾀ033','TP332','D','D','D','routeLift1','suppl','高木製作所','store2',54,0,0,'fafacc',50,119,'2025/10/16 14:45:00','2025/10/16 14:45:00'),('57643-42010','ｵ068','TP332','D','D','D','routeLift1','suppl','岡本工業','store2',54,0,0,'fafacc',80,120,'2025/10/16 13:37:00','2025/10/16 13:37:00'),('57644-42010','ｵ069','TP332','D','D','D','routeLift1','suppl','岡本工業','store2',54,0,0,'fafacc',80,121,'2025/10/16 14:46:00','2025/10/16 14:46:00'),('57703-42031','T703','TP362','D','D','D','routeLift1','suppl','豊鉄細谷','store2',54,0,0,'fafacc',5,122,'2025/10/16 13:31:00','2025/10/16 13:31:00'),('57704-42031','T704','TP332','D','D','D','routeLift1','suppl','豊鉄細谷','store2',54,0,0,'fafacc',5,123,'2025/10/16 13:43:00','2025/10/16 15:05:00'),('57721-42060','513K','A','A','A','A','routeLift1','suppl','幸工','store2',54,0,0,'fafacc',300,126,'2025/10/16 13:34:00','2025/10/16 13:34:00'),('57721-42060-','5130','A','A','A','A','routeLift1','suppl','幸工','store2',54,0,0,'fafacc',300,124,'2025/10/16 13:34:00','2025/10/16 13:34:00'),('57722-42060','514K','A','A','A','A','routeLift1','suppl','幸工','store2',54,0,0,'fafacc',300,127,'2025/10/16 14:43:00','2025/10/16 14:43:00'),('57722-42060-','5140','A','A','A','A','routeLift1','suppl','幸工','store2',54,0,0,'fafacc',300,125,'2025/10/16 14:43:00','2025/10/16 14:43:00'),('57735-42060','ｵ070','TP332','D','D','D','routeLift1','suppl','岡本工業','store2',54,0,0,'fafacc',40,129,'2025/10/16 15:02:00','2025/10/16 15:02:00'),('57736-42060','ｵ071','TP332','D','D','D','routeLift1','suppl','岡本工業','store2',54,0,0,'fafacc',40,130,'2025/10/16 14:44:00','2025/10/16 14:44:00');
/*!40000 ALTER TABLE `m_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `m_product_inventory`
--

DROP TABLE IF EXISTS `m_product_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_product_inventory` (
  `part_number` varchar(20) NOT NULL,
  `part_deferment` int DEFAULT NULL,
  `part_limit` int DEFAULT NULL,
  `innner_parts` int DEFAULT NULL,
  PRIMARY KEY (`part_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_product_inventory`
--

LOCK TABLES `m_product_inventory` WRITE;
/*!40000 ALTER TABLE `m_product_inventory` DISABLE KEYS */;
INSERT INTO `m_product_inventory` VALUES ('1001-0001',600,300,10),('1001-0002',600,300,2),('1002-0001',600,300,1),('1002-0002',600,300,1),('1003-0001',600,300,1),('1004-0001',600,300,1),('1005-0001',600,300,1),('1006-0001',600,300,1),('1006-0002',600,300,1),('1006-0003',600,300,1),('1007-0001',600,300,1),('1008-0001',600,300,1),('1009-0001',600,300,1),('1010-0001',600,300,1),('1011-0001',600,300,1),('57413-42090',600,300,200),('57413-42100-',600,300,200),('57414-42090',600,300,200),('57414-42100',600,300,200),('57415-42040',600,300,100),('57416-42030',600,300,100),('57435-42010',600,300,30),('57436-42010',600,300,30),('57607-42090',600,300,18),('57611-42070-',600,300,70),('57612-42070-',600,300,70),('57621-42010',600,300,40),('57622-42010',600,300,40),('57631-42020',600,300,16),('57632-42060',600,300,16),('57637-42070',600,300,40),('57638-42050',600,300,40),('57641-42030',600,300,50),('57642-42030',600,300,50),('57643-42010',600,300,80),('57644-42010',600,300,80),('57703-42031',600,300,5),('57704-42031',600,300,5),('57721-42060',600,300,300),('57721-42060-',600,300,300),('57722-42060',600,300,300),('57722-42060-',600,300,300),('57735-42060',600,300,40),('57736-42060',600,300,40),('90174-08010',600,300,1500),('94223-80600',600,300,4000),('94223-80800',600,300,2500),('94228-11200',600,300,400);
/*!40000 ALTER TABLE `m_product_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `position` (
  `rack_id` int NOT NULL,
  PRIMARY KEY (`rack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `position`
--

LOCK TABLES `position` WRITE;
/*!40000 ALTER TABLE `position` DISABLE KEYS */;
INSERT INTO `position` VALUES (1),(2),(3),(4);
/*!40000 ALTER TABLE `position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production`
--

DROP TABLE IF EXISTS `production`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `production` (
  `product_id` varchar(20) NOT NULL,
  `time_stamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`,`time_stamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production`
--

LOCK TABLES `production` WRITE;
/*!40000 ALTER TABLE `production` DISABLE KEYS */;
INSERT INTO `production` VALUES ('1111','2025-09-01 00:00:00'),('1111','2025-09-26 16:16:16'),('1111','2025-09-26 16:16:25'),('1111','2025-10-12 11:11:11'),('1111-1111','2025-10-24 13:36:02'),('1111-1111','2025-10-24 13:36:23'),('1111-1111','2025-10-24 13:38:42'),('1111-1111','2025-10-24 13:39:04'),('1111-1111','2025-10-28 14:34:26');
/*!40000 ALTER TABLE `production` ENABLE KEYS */;
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
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `production_AFTER_INSERT` AFTER INSERT ON `production` FOR EACH ROW BEGIN

DECLARE id INT default 0;
DECLARE total INT default 0;
DECLARE case_total INT default 0;
DECLARE done INT DEFAULT FALSE;

DECLARE cur_inventory CURSOR FOR
	SELECT inventory_id,(part_quantity-quantity) as t,CEILING((part_quantity-quantity)/innner_parts) as c 
    FROM depal.futaba_product
    inner join depal.line_product using(product_id)
	inner join depal.line_frontage using(line_id)
	inner join depal.line_inventory using(frontage_id)
    inner join depal.composition using(product_id,part_number)
    inner join depal.m_product using(part_number)
    inner join depal.m_product_inventory using(part_number)
	where product_id=new.product_id;
    
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

OPEN cur_inventory;

loop1: LOOP    
	FETCH cur_inventory INTO  id,total,case_total; 
	IF done THEN
      LEAVE loop1;
    END IF;
	UPDATE depal.line_inventory set case_quantity=case_total,part_quantity=total,update_date=new.time_stamp
	WHERE depal.line_inventory.inventory_id=id;
    
END LOOP loop1;
    
CLOSE cur_inventory;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `rack_position`
--

DROP TABLE IF EXISTS `rack_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rack_position` (
  `inventory_id` int NOT NULL,
  `rack_id` int NOT NULL,
  PRIMARY KEY (`inventory_id`,`rack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rack_position`
--

LOCK TABLES `rack_position` WRITE;
/*!40000 ALTER TABLE `rack_position` DISABLE KEYS */;
INSERT INTO `rack_position` VALUES (1,1),(2,3),(3,1),(4,1),(5,2),(6,2),(7,4),(8,1),(9,2),(10,1);
/*!40000 ALTER TABLE `rack_position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signal`
--

DROP TABLE IF EXISTS `signal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `signal` (
  `signal_id` int NOT NULL,
  `frontage_id` int NOT NULL,
  `tag` varchar(40) NOT NULL,
  PRIMARY KEY (`signal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signal`
--

LOCK TABLES `signal` WRITE;
/*!40000 ALTER TABLE `signal` DISABLE KEYS */;
INSERT INTO `signal` VALUES (8000,1,'flow_rack_request'),(8001,1,'kotatsu_request'),(8002,1,'dispatch'),(8003,1,'fetch1'),(8005,1,'fetch2'),(8007,1,'fetch3'),(8009,1,'fetch4'),(8011,1,'fetch5'),(8013,1,'fetch6'),(8015,2,'flow_rack_request'),(8016,2,'kotatsu_request'),(8017,2,'dispatch'),(8018,2,'fetch1'),(8020,2,'fetch2'),(8022,2,'fetch3'),(8024,2,'fetch4'),(8026,2,'fetch5'),(8028,2,'fetch6'),(8030,3,'flow_rack_request'),(8031,3,'kotatsu_request'),(8032,3,'dispatch'),(8033,3,'fetch1'),(8035,3,'fetch2'),(8037,3,'fetch3'),(8039,3,'fetch4'),(8041,3,'fetch5'),(8043,3,'fetch6'),(8045,4,'flow_rack_request'),(8046,4,'kotatsu_request'),(8047,4,'dispatch'),(8048,4,'fetch1'),(8050,4,'fetch2'),(8052,4,'fetch3'),(8054,4,'fetch4'),(8056,4,'fetch5'),(8058,4,'fetch6'),(8060,5,'flow_rack_request'),(8061,5,'kotatsu_request'),(8062,5,'dispatch'),(8063,5,'fetch1'),(8065,5,'fetch2'),(8067,5,'fetch3'),(8069,5,'fetch4'),(8071,5,'fetch5'),(8073,5,'fetch6'),(8100,1,'ready'),(8101,2,'ready'),(8102,3,'ready'),(8103,4,'ready'),(8104,5,'ready'),(8105,1,'part1_no'),(8106,1,'part1_count'),(8107,1,'part2_no'),(8108,1,'part2_count'),(8109,1,'part3_no'),(8110,1,'part3_count'),(8111,1,'part4_no'),(8112,1,'part4_count'),(8113,1,'part5_no'),(8114,1,'part5_count'),(8115,1,'part6_no'),(8116,1,'part6_count'),(8117,2,'part1_no'),(8118,2,'part1_count'),(8119,2,'part2_no'),(8120,2,'part2_count'),(8121,2,'part3_no'),(8122,2,'part3_count'),(8123,2,'part4_no'),(8124,2,'part4_count'),(8125,2,'part5_no'),(8126,2,'part5_count'),(8127,2,'part6_no'),(8128,2,'part6_count'),(8129,3,'part1_no'),(8130,3,'part1_count'),(8131,3,'part2_no'),(8132,3,'part2_count'),(8133,3,'part3_no'),(8134,3,'part3_count'),(8135,3,'part4_no'),(8136,3,'part4_count'),(8137,3,'part5_no'),(8138,3,'part5_count'),(8139,3,'part6_no'),(8140,3,'part6_count'),(8141,4,'part1_no'),(8142,4,'part1_count'),(8143,4,'part2_no'),(8144,4,'part2_count'),(8145,4,'part3_no'),(8146,4,'part3_count'),(8147,4,'part4_no'),(8148,4,'part4_count'),(8149,4,'part5_no'),(8150,4,'part5_count'),(8151,4,'part6_no'),(8152,4,'part6_count'),(8153,5,'part1_no'),(8154,5,'part1_count'),(8155,5,'part2_no'),(8156,5,'part2_count'),(8157,5,'part3_no'),(8158,5,'part3_count'),(8159,5,'part4_no'),(8160,5,'part4_count'),(8161,5,'part5_no'),(8162,5,'part5_count'),(8163,5,'part6_no'),(8164,5,'part6_count'),(8400,1,'model_id'),(8401,2,'model_id'),(8402,3,'model_id'),(8403,4,'model_id'),(8404,5,'model_id'),(8405,1,'fetch1_count'),(8406,1,'fetch2_count'),(8407,1,'fetch3_count'),(8408,1,'fetch4_count'),(8409,1,'fetch5_count'),(8410,1,'fetch6_count'),(8411,2,'fetch1_count'),(8412,2,'fetch2_count'),(8413,2,'fetch3_count'),(8414,2,'fetch4_count'),(8415,2,'fetch5_count'),(8416,2,'fetch6_count'),(8417,3,'fetch1_count'),(8418,3,'fetch2_count'),(8419,3,'fetch3_count'),(8420,3,'fetch4_count'),(8421,3,'fetch5_count'),(8422,3,'fetch6_count'),(8423,4,'fetch1_count'),(8424,4,'fetch2_count'),(8425,4,'fetch3_count'),(8426,4,'fetch4_count'),(8427,4,'fetch5_count'),(8428,4,'fetch6_count'),(8429,5,'fetch1_count'),(8430,5,'fetch2_count'),(8431,5,'fetch3_count'),(8432,5,'fetch4_count'),(8433,5,'fetch5_count'),(8434,5,'fetch6_count');
/*!40000 ALTER TABLE `signal` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Dumping events for database 'depal'
--

--
-- Dumping routines for database 'depal'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-17 16:24:38
