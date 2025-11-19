CREATE SCHEMA `depal` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;

DROP TABLE IF EXISTS `composition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `composition` (
  `product_id` varchar(20) NOT NULL,
  `part_number` varchar(20) NOT NULL,
  `quantity_per_product` varchar(45) NOT NULL,
  PRIMARY KEY (`product_id`,`part_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `depallet_area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `depallet_area` (
  `area_id` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`area_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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

DROP TABLE IF EXISTS `futaba_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `futaba_product` (
  `product_id` varchar(20) NOT NULL,
  `kanban_no` varchar(10) NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `line_depallet_frontage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `line_depallet_frontage` (
  `line_id` int NOT NULL,
  `frontage_id` int NOT NULL,
  PRIMARY KEY (`line_id`,`frontage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `line_frontage`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `line_frontage` (
  `frontage_id` int NOT NULL,
  `line_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `cell_code` varchar(8) NOT NULL,
  `car_model_id` int NOT NULL,
  PRIMARY KEY (`frontage_id`),
  KEY `line_idx` (`line_id`),
  KEY `line_99_idx` (`line_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
  KEY `part_idx` (`part_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `line_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `line_product` (
  `line_id` int NOT NULL,
  `product_id` varchar(20) NOT NULL,
  PRIMARY KEY (`line_id`,`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `line` (
  `line_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `process` varchar(10) NOT NULL,
  PRIMARY KEY (`line_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `m_product_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_product_inventory` (
  `part_number` varchar(20) NOT NULL,
  `part_deferment` int DEFAULT NULL,
  `part_limit` int DEFAULT NULL,
  `innner_parts` int DEFAULT NULL,
  PRIMARY KEY (`part_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `position` (
  `rack_position_id` int NOT NULL,
  PRIMARY KEY (`rack_position_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `production`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `production` (
  `product_id` varchar(20) NOT NULL,
  `time_stamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`,`time_stamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `rack_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rack_position` (
  `inventory_id` int NOT NULL,
  `rack_position_id` int NOT NULL,
  PRIMARY KEY (`inventory_id`,`rack_position_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `signal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `signal` (
  `signal_id` int NOT NULL,
  `frontage_id` int NOT NULL,
  `tag` varchar(40) NOT NULL,
  PRIMARY KEY (`signal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `parts_supply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parts_supply` (
  `inventory_id` int NOT NULL,
  `time_stamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `case_quantity` int NOT NULL,
  PRIMARY KEY (`inventory_id`,`time_stamp`),
  KEY `line_inventory_idx` (`inventory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
























