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
  KEY `line_99_idx` (`line_id`),
  CONSTRAINT `line_99` FOREIGN KEY (`line_id`) REFERENCES `line` (`line_id`)
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
  KEY `part_idx` (`part_number`),
  CONSTRAINT `frontage` FOREIGN KEY (`frontage_id`) REFERENCES `line_frontage` (`frontage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `parts_supply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parts_supply` (
  `inventory_id` int NOT NULL,
  `time_stamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `case_quantity` int NOT NULL,
  PRIMARY KEY (`inventory_id`,`time_stamp`),
  KEY `line_inventory_idx` (`inventory_id`),
  CONSTRAINT `line_inventory` FOREIGN KEY (`inventory_id`) REFERENCES `line_inventory` (`inventory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
