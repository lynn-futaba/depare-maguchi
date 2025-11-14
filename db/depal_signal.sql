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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 12:58:35
