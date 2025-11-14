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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 12:58:34
