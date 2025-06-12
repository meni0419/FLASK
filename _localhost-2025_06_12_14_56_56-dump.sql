/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: flask_ich
-- ------------------------------------------------------
-- Server version	10.11.13-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `address_id` int(11) NOT NULL AUTO_INCREMENT,
  `city` varchar(255) DEFAULT NULL CHECK (octet_length(`city`) >= 2),
  `street` varchar(255) DEFAULT NULL CHECK (octet_length(`street`) >= 3),
  `house_number` int(11) DEFAULT NULL CHECK (`house_number` > 0),
  PRIMARY KEY (`address_id`),
  KEY `idx_addresses_city` (`city`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES
(1,'Київ','Володимирська',15),
(2,'Львів','Шевченка',25),
(3,'Івано-Франківськ','Незалежності',17),
(4,'Одеса','Дерибасівська',12),
(5,'Харків','Сумська',40),
(6,'Дніпро','Пушкіна',8),
(7,'Тернопіль','Бандери',22),
(8,'Чернівці','Головна',13),
(9,'Ужгород','Корзо',7),
(10,'Луцьк','Винниченка',19),
(11,'Полтава','Європейська',21),
(12,'Запоріжжя','Соборна',30),
(13,'Житомир','Київська',10),
(14,'Ancara','Postovaya',10),
(15,'New York','5th Avenue',123);
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_uuid` char(36) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL,
  `status` int(11) DEFAULT 1,
  `is_admin` tinyint(1) DEFAULT 0,
  `age` int(11) DEFAULT NULL CHECK (`age` between 0 and 120),
  `is_employed` tinyint(1) DEFAULT 0,
  `address_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_uuid`),
  KEY `idx_users_address` (`address_id`),
  KEY `idx_users_username` (`username`),
  CONSTRAINT `fk_user_address` FOREIGN KEY (`address_id`) REFERENCES `addresses` (`address_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
('1cfc5792-e59b-42f4-87f2-114916f1a8ee','admin_boss','boss@example.com','21232f297a57a5a743894a0e4a801fc3','Admin Chief','2025-06-12 10:45:51','2025-06-12 10:23:20',1,1,25,0,1),
('29c1302e-11fe-4922-85dd-3f146bd4369d','banny_doe','banny.doe@example.com','$2b$12$TPC9fi5Et6fZfD/jdFQyVuoTuuD57vcSfPopB.bIOJk1SLry2EDfG','Banny Doe','2025-06-12 09:49:00','2025-06-12 11:43:41',1,0,70,1,15),
('31a3d0b8-2d7f-4bb1-aadf-019172f6a30f','tech_guru','guru@tech.org','b2e98ad6f6eb8508dd6a14cfa704bad7','Tech Guru','2025-06-12 10:45:51',NULL,1,0,NULL,0,2),
('3c24fbc2-26f1-4287-8310-d27e53ed2b58','john_doe','john@example.com','$2b$12$3nZvP1FiPusp2Z7H6xWlc.C88h21J6acnHtHjBC2isvcatXXv5ZLy','John Doe','2025-06-12 09:27:33',NULL,1,0,25,1,14),
('3e153586-4b45-4df7-8935-9dc654d8ebfc','alex_snake',NULL,'fcea920f7412b5da7be0cf42b8c93759','Alex Snake','2025-06-12 10:45:51',NULL,1,0,NULL,0,3),
('4fd89d13-1f57-4f03-a4c0-411129b2d501','mmaximus','max@example.com','9b74c9897bac770ffc029102a200c5de','Максим Коваленко','2025-06-12 10:45:51',NULL,1,0,NULL,0,4),
('550e8400-e29b-41d4-a716-446655440000','mmaximus','max@example.com','9b74c9897bac770ffc029102a200c5de','Максим Коваленко','2025-06-12 10:45:09',NULL,1,0,NULL,0,5),
('6f1e9be3-4b39-4e30-a6f3-faf918719b57','jane_doe','jane@example.com','5f4dcc3b5aa765d61d8327deb882cf99','Jane Doe','2025-06-12 10:45:09',NULL,1,1,NULL,0,6),
('6fce633e-faa6-49fd-a8eb-2e66558d298b','john_dev',NULL,'3f230640b78d7e71ac5514e57935eb69','John Developer','2025-06-12 10:45:51',NULL,1,0,NULL,0,7),
('79a1fe91-d5d4-47b4-9d32-1f9a0a00aa3b','dev_guy',NULL,'3f230640b78d7e71ac5514e57935eb69','John Dev','2025-06-12 10:45:09',NULL,0,0,NULL,0,8),
('8f703ee8-4d6a-44bb-9c6a-0e4bb21b1030','natalie_voice','natalie@voicelab.com','c33367701511b4f6020ec61ded352059','Наталья Голосова','2025-06-12 10:45:51',NULL,1,0,NULL,0,9),
('a92ab153-d52a-422f-a437-bf5f92635b4d','lena_art','lena@artmail.com','098f6bcd4621d373cade4e832627b4f6','Лена Артюх','2025-06-12 10:45:51',NULL,0,0,NULL,0,10),
('c0a6026b-3fd2-43c1-bf8f-0b2f9a4e6f85','jane_doe','jane@example.com','5f4dcc3b5aa765d61d8327deb882cf99','Jane Doe','2025-06-12 10:45:51',NULL,1,1,NULL,0,11),
('cbb2c10d-47c6-4b6a-94d7-08bb195e9334','kate_writer','kate@words.net','827ccb0eea8a706c4c34a16891f84e7b','Kate Writer','2025-06-12 10:45:51',NULL,0,0,NULL,0,12),
('ff4d984a-81a1-4d64-af79-261abac421c4','maria_msk','maria@mail.ru','e99a18c428cb38d5f260853678922e03','Мария Иванова','2025-06-12 10:45:51',NULL,1,0,NULL,0,13);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-12 14:56:56
