-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: course_center
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

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
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `grade_id` int(11) NOT NULL,
  `absence_date` date DEFAULT NULL,
  `absence_day` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `attendance_student_id` (`student_id`),
  KEY `attendance_course_id` (`course_id`),
  KEY `attendance_teacher_id` (`teacher_id`),
  KEY `attendance_grade_id` (`grade_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `attendance_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`),
  CONSTRAINT `attendance_ibfk_4` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `grade_id` int(11) NOT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_name_grade_id_teacher_id` (`name`,`grade_id`,`teacher_id`),
  KEY `course_grade_id` (`grade_id`),
  KEY `course_teacher_id` (`teacher_id`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`),
  CONSTRAINT `course_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'لغة عربية',1,1,500.00),(2,'لغة انجليزية',1,2,500.00),(3,'رياضيات',1,3,500.00),(5,'لغة عربية',2,1,500.00),(6,'لغة انجليزية',2,2,500.00),(7,'رياضيات',2,3,500.00),(8,'لغة عربية',3,1,500.00),(9,'لغة انجليزية',3,2,500.00),(10,'رياضيات',3,3,500.00),(11,'لغة عربية',4,4,800.00),(12,'لغة انجليزية',4,5,800.00),(13,'رياضيات',4,9,800.00),(14,'لغة عربية',5,4,800.00),(15,'لغة انجليزية',5,5,800.00),(16,'رياضيات',5,9,800.00),(17,'لغة عربية',7,4,800.00),(18,'لغة انجليزية',7,5,800.00),(19,'رياضيات',7,9,800.00);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollment`
--

DROP TABLE IF EXISTS `enrollment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enrollment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `grade_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `month` varchar(15) DEFAULT NULL,
  `course_price` decimal(10,2) NOT NULL,
  `late_registration` tinyint(1) NOT NULL,
  `withdrawn` tinyint(1) NOT NULL,
  `center_share` decimal(10,2) NOT NULL,
  `attendance_count` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `enrollment_student_id` (`student_id`),
  KEY `enrollment_teacher_id` (`teacher_id`),
  KEY `enrollment_grade_id` (`grade_id`),
  KEY `enrollment_course_id` (`course_id`),
  KEY `enrollment_user_id` (`user_id`),
  CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`),
  CONSTRAINT `enrollment_ibfk_3` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`),
  CONSTRAINT `enrollment_ibfk_4` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `enrollment_ibfk_5` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollment`
--

LOCK TABLES `enrollment` WRITE;
/*!40000 ALTER TABLE `enrollment` DISABLE KEYS */;
INSERT INTO `enrollment` VALUES (1,1,1,1,1,'أكتوبر',250.00,1,0,0.00,4,1),(2,2,1,1,1,'أكتوبر',250.00,1,0,0.00,4,1),(3,2,2,1,2,'أكتوبر',250.00,1,0,0.00,4,1),(5,3,1,1,1,'أكتوبر',500.00,0,0,0.00,0,1),(6,3,2,1,2,'أكتوبر',500.00,0,0,0.00,0,1),(7,3,3,1,3,'أكتوبر',500.00,0,0,0.00,0,1),(8,9,4,4,11,'أكتوبر',400.00,0,1,200.00,4,1),(9,9,5,4,12,'أكتوبر',500.00,0,1,312.50,5,1),(10,9,9,4,13,'أكتوبر',300.00,0,1,112.50,3,1),(11,1,2,1,2,'أكتوبر',250.00,1,0,0.00,4,1),(12,4,1,2,5,'أكتوبر',500.00,0,0,250.00,0,1),(13,4,2,2,6,'أكتوبر',500.00,0,0,250.00,0,1),(14,10,4,4,11,'أكتوبر',800.00,0,0,320.00,0,1),(15,10,5,4,12,'أكتوبر',800.00,0,0,320.00,0,1),(16,5,1,2,5,'أكتوبر',250.00,1,0,125.00,4,1),(17,6,1,2,5,'أكتوبر',250.00,0,1,250.00,4,1),(18,6,2,2,6,'أكتوبر',250.00,0,1,250.00,4,1),(19,7,1,3,8,'أكتوبر',250.00,0,1,250.00,4,1),(20,7,2,3,9,'أكتوبر',250.00,0,1,250.00,4,1),(21,8,1,3,8,'أكتوبر',250.00,0,1,125.00,4,1),(22,8,3,3,10,'أكتوبر',250.00,0,1,125.00,4,1),(23,11,4,4,11,'أكتوبر',500.00,0,1,312.50,5,1),(24,11,9,4,13,'أكتوبر',400.00,0,1,200.00,4,1),(25,13,4,5,14,'أكتوبر',500.00,0,1,312.50,5,1),(26,13,9,5,16,'أكتوبر',400.00,0,1,200.00,4,1),(27,14,4,5,14,'أكتوبر',500.00,0,1,312.50,5,1),(28,14,9,5,16,'أكتوبر',400.00,0,1,200.00,4,1),(29,15,4,7,17,'أكتوبر',400.00,0,1,200.00,4,1),(30,15,5,7,18,'أكتوبر',400.00,0,1,200.00,4,1),(31,16,5,7,18,'أكتوبر',400.00,0,1,200.00,4,1),(32,16,9,7,19,'أكتوبر',400.00,0,1,200.00,4,1),(33,17,4,7,17,'أكتوبر',400.00,0,1,160.00,4,1),(34,17,9,7,19,'أكتوبر',400.00,0,1,160.00,4,1),(35,12,4,5,14,'أكتوبر',400.00,1,0,160.00,4,1),(36,12,9,5,16,'أكتوبر',500.00,1,0,200.00,5,1);
/*!40000 ALTER TABLE `enrollment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grade`
--

DROP TABLE IF EXISTS `grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grade` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `level` varchar(255) DEFAULT NULL,
  `term` varchar(255) DEFAULT NULL,
  `academic_year` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `grade_name_level_term_academic_year` (`name`,`level`,`term`,`academic_year`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grade`
--

LOCK TABLES `grade` WRITE;
/*!40000 ALTER TABLE `grade` DISABLE KEYS */;
INSERT INTO `grade` VALUES (1,'الأول','الإعدادية','الأول','2025/2026'),(2,'الثاني','الإعدادية','الأول','2025/2026'),(3,'الثالث','الإعدادية','الأول','2025/2026'),(4,'الأول','الثانوية','الأول','2025/2026'),(5,'الثاني','الثانوية','الأول','2025/2026'),(7,'الثالث','الثانوية','الأول','2025/2026');
/*!40000 ALTER TABLE `grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `management`
--

DROP TABLE IF EXISTS `management`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `management` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prime_st_account` int(11) NOT NULL,
  `prep_st_account` int(11) NOT NULL,
  `sec_st_account` int(11) NOT NULL,
  `outcome` decimal(14,2) NOT NULL,
  `share_percent` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `management`
--

LOCK TABLES `management` WRITE;
/*!40000 ALTER TABLE `management` DISABLE KEYS */;
/*!40000 ALTER TABLE `management` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `cash_back` decimal(10,2) NOT NULL,
  `center_share` decimal(10,2) NOT NULL,
  `paid_type` varchar(255) NOT NULL,
  `payment_date` date NOT NULL,
  `month` varchar(15) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_student_id` (`student_id`),
  KEY `payment_user_id` (`user_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (2,1,200.00,0.00,0.00,'نقدي','2025-10-17','أكتوبر',1),(3,3,500.00,0.00,0.00,'نقدي','2025-10-18','أكتوبر',1),(4,4,500.00,0.00,250.00,'نقدي','2025-10-18','أكتوبر',1),(5,4,500.00,0.00,250.00,'نقدي','2025-10-18','أكتوبر',1),(6,10,500.00,0.00,200.00,'نقدي','2025-10-18','أكتوبر',1),(7,5,250.00,0.00,125.00,'نقدي','2025-10-19','أكتوبر',1),(8,2,500.00,0.00,0.00,'نقدي','2025-10-19','أكتوبر',1),(9,6,1000.00,0.00,500.00,'نقدي','2025-10-19','أكتوبر',1),(10,7,1000.00,0.00,500.00,'نقدي','2025-10-19','أكتوبر',1),(11,8,1000.00,0.00,500.00,'نقدي','2025-10-19','أكتوبر',1),(12,9,2400.00,0.00,0.00,'نقدي','2025-10-19','أكتوبر',1),(13,11,1600.00,0.00,640.00,'نقدي','2025-10-19','أكتوبر',1),(14,13,900.00,0.00,512.50,'نقدي','2025-10-19','أكتوبر',1),(15,14,900.00,700.00,512.50,'نقدي','2025-10-19','أكتوبر',1),(16,15,800.00,200.00,400.00,'نقدي','2025-10-20','أكتوبر',1),(17,16,800.00,200.00,400.00,'نقدي','2025-10-20','أكتوبر',1),(18,17,800.00,0.00,320.00,'نقدي','2025-10-20','أكتوبر',1),(19,12,500.00,0.00,200.00,'نقدي','2025-10-20','أكتوبر',1),(20,12,400.00,0.00,160.00,'نقدي','2025-10-20','أكتوبر',1);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_tab` tinyint(1) NOT NULL,
  `teacher_tab` tinyint(1) NOT NULL,
  `grade_tab` tinyint(1) NOT NULL,
  `course_tab` tinyint(1) NOT NULL,
  `student_tab` tinyint(1) NOT NULL,
  `enrollment_tab` tinyint(1) NOT NULL,
  `student_account_tab` tinyint(1) NOT NULL,
  `student_stat_tab` tinyint(1) NOT NULL,
  `teacher_account_tab` tinyint(1) NOT NULL,
  `attendance_tab` tinyint(1) NOT NULL,
  `management_tab` tinyint(1) NOT NULL,
  `permission_tab` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `permission_user_id` (`user_id`),
  CONSTRAINT `permission_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,1,1,1,1,1,1,1,1,1,1,1,1,1),(2,3,1,1,1,0,0,1,0,0,0,1,0,0);
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `grade_id` int(11) NOT NULL,
  `section` int(11) DEFAULT NULL,
  `reg_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_phone` (`phone`),
  KEY `student_grade_id` (`grade_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'هاني خليل عبد اللطيف','01035795125',1,1,'2025-10-14 00:00:00'),(2,'عبد المجيد احمد السيد','01196548521',1,1,'2025-10-14 00:00:00'),(3,'حامد السيد جلال','01552146987',1,1,'2025-10-14 00:00:00'),(4,'خالد فتحي رجب','01575395145',2,1,'2025-10-14 00:00:00'),(5,'علي رجب محمد','01565412398',2,1,'2025-10-14 00:00:00'),(6,'ممدوح محمد جعفر','01296541238',2,1,'2025-10-14 00:00:00'),(7,'هلال خالد صبري','01545698712',3,1,'2025-10-14 00:00:00'),(8,'جمال السيد حامد','01222336548',3,1,'2025-10-14 00:00:00'),(9,'منى السيد خليل','01555896321',4,1,'2025-10-14 00:00:00'),(10,'ياسر علي شريف','01000365248',4,1,'2025-10-14 00:00:00'),(11,'هادي محمد احمد','01119523485',4,1,'2025-10-14 00:00:00'),(12,'جمال احمد السيد','01000524691',5,1,'2025-10-15 00:00:00'),(13,'سمير هاني خالد','01200063584',5,1,'2025-10-15 00:00:00'),(14,'فؤاد محمد السيد','01500096325',5,1,'2025-10-15 00:00:00'),(15,'حبيب خالد جمال','01010063584',7,1,'2025-10-15 00:00:00'),(16,'يحيى يوسف جلال','01111336528',7,1,'2025-10-15 00:00:00'),(17,'غدير محمد صلاح','01515158253',7,1,'2025-10-15 00:00:00');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentmonthlyinvoice`
--

DROP TABLE IF EXISTS `studentmonthlyinvoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `studentmonthlyinvoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `month` varchar(15) DEFAULT NULL,
  `total_due` decimal(10,2) NOT NULL,
  `total_paid` decimal(10,2) NOT NULL,
  `remain` decimal(10,2) NOT NULL,
  `course_count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `studentmonthlyinvoice_student_id` (`student_id`),
  CONSTRAINT `studentmonthlyinvoice_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentmonthlyinvoice`
--

LOCK TABLES `studentmonthlyinvoice` WRITE;
/*!40000 ALTER TABLE `studentmonthlyinvoice` DISABLE KEYS */;
INSERT INTO `studentmonthlyinvoice` VALUES (1,1,'أكتوبر',500.00,200.00,300.00,2),(2,2,'أكتوبر',500.00,500.00,0.00,2),(3,3,'أكتوبر',1500.00,500.00,1000.00,3),(4,9,'أكتوبر',1200.00,2400.00,-1200.00,3),(5,4,'أكتوبر',1000.00,1000.00,0.00,2),(6,10,'أكتوبر',1600.00,500.00,1100.00,2),(7,5,'أكتوبر',250.00,250.00,0.00,1),(8,6,'أكتوبر',500.00,1000.00,-500.00,2),(9,7,'أكتوبر',500.00,1000.00,-500.00,2),(10,8,'أكتوبر',500.00,1000.00,-500.00,2),(11,11,'أكتوبر',900.00,1600.00,-700.00,2),(12,13,'أكتوبر',900.00,1600.00,-700.00,2),(13,14,'أكتوبر',900.00,1600.00,-700.00,2),(14,15,'أكتوبر',800.00,1000.00,-200.00,2),(15,16,'أكتوبر',800.00,1000.00,-200.00,2),(16,17,'أكتوبر',800.00,800.00,0.00,2),(17,12,'أكتوبر',900.00,900.00,0.00,2);
/*!40000 ALTER TABLE `studentmonthlyinvoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `share_percent` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `teacher_phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES (1,'سمير محمد علي','01145632178','لغة عربية - إعدادي',50.00),(2,'احمد علي ابراهيم','01285214796','لغة انجليزية - إعدادي',50.00),(3,'محمد خليل سامي','01545632195','رياضيات - إعدادي',50.00),(4,'خالد محمد حامد','01085214763','لغة عربية - ثانوي',60.00),(5,'ياسر خليل محمد','01545698521','لغة انجليزية - ثانوي',60.00),(9,'علي فايد يسري','01185236941','رياضيات - ثانوي',60.00);
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacheraccount`
--

DROP TABLE IF EXISTS `teacheraccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacheraccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `income` decimal(10,2) NOT NULL,
  `month` varchar(15) DEFAULT NULL,
  `student_count` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `date` date NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `teacheraccount_teacher_id` (`teacher_id`),
  KEY `teacheraccount_user_id` (`user_id`),
  CONSTRAINT `teacheraccount_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`),
  CONSTRAINT `teacheraccount_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacheraccount`
--

LOCK TABLES `teacheraccount` WRITE;
/*!40000 ALTER TABLE `teacheraccount` DISABLE KEYS */;
INSERT INTO `teacheraccount` VALUES (1,1,1250.00,'أكتوبر',8,0,'2025-10-15',NULL),(2,2,1000.00,'أكتوبر',6,0,'2025-10-15',NULL),(3,3,375.00,'أكتوبر',2,0,'2025-10-15',NULL),(4,4,2340.00,'أكتوبر',8,0,'2025-10-16',NULL),(5,5,1260.00,'أكتوبر',4,0,'2025-10-16',NULL),(6,9,1680.00,'أكتوبر',7,0,'2025-10-16',NULL);
/*!40000 ALTER TABLE `teacheraccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachercourse`
--

DROP TABLE IF EXISTS `teachercourse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teachercourse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `teachercourse_teacher_id` (`teacher_id`),
  KEY `teachercourse_course_id` (`course_id`),
  CONSTRAINT `teachercourse_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`),
  CONSTRAINT `teachercourse_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachercourse`
--

LOCK TABLES `teachercourse` WRITE;
/*!40000 ALTER TABLE `teachercourse` DISABLE KEYS */;
/*!40000 ALTER TABLE `teachercourse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacherstudent`
--

DROP TABLE IF EXISTS `teacherstudent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacherstudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `grade_id` int(11) NOT NULL,
  `month` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `teacherstudent_teacher_id` (`teacher_id`),
  KEY `teacherstudent_student_id` (`student_id`),
  KEY `teacherstudent_grade_id` (`grade_id`),
  CONSTRAINT `teacherstudent_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`),
  CONSTRAINT `teacherstudent_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `teacherstudent_ibfk_3` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacherstudent`
--

LOCK TABLES `teacherstudent` WRITE;
/*!40000 ALTER TABLE `teacherstudent` DISABLE KEYS */;
INSERT INTO `teacherstudent` VALUES (1,1,1,1,'أكتوبر'),(2,1,2,1,'أكتوبر'),(3,2,2,1,'أكتوبر'),(5,1,3,1,'أكتوبر'),(6,2,3,1,'أكتوبر'),(7,3,3,1,'أكتوبر'),(8,4,9,4,'أكتوبر'),(9,5,9,4,'أكتوبر'),(10,9,9,4,'أكتوبر'),(11,2,1,1,'أكتوبر'),(12,1,4,2,'أكتوبر'),(13,2,4,2,'أكتوبر'),(14,4,10,4,'أكتوبر'),(15,5,10,4,'أكتوبر'),(16,1,5,2,'أكتوبر'),(17,1,6,2,'أكتوبر'),(18,2,6,2,'أكتوبر'),(19,1,7,3,'أكتوبر'),(20,2,7,3,'أكتوبر'),(21,1,8,3,'أكتوبر'),(22,3,8,3,'أكتوبر'),(23,4,11,4,'أكتوبر'),(24,9,11,4,'أكتوبر'),(25,4,13,5,'أكتوبر'),(26,9,13,5,'أكتوبر'),(27,4,14,5,'أكتوبر'),(28,9,14,5,'أكتوبر'),(29,4,15,7,'أكتوبر'),(30,5,15,7,'أكتوبر'),(31,5,16,7,'أكتوبر'),(32,9,16,7,'أكتوبر'),(33,4,17,7,'أكتوبر'),(34,9,17,7,'أكتوبر'),(35,4,12,5,'أكتوبر'),(36,9,12,5,'أكتوبر');
/*!40000 ALTER TABLE `teacherstudent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `job` varchar(50) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_username` (`username`),
  UNIQUE KEY `user_phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'mostafa','$2b$12$7yP0fBSvnsxdxG3z4O34YeoSZnZottFgSzVf330WcZgG0UVWkRfn2','مصطفى بسيوني','01099231700','المدير العام',1,'2025-10-13 00:00:00'),(3,'amera','$2b$12$rZPyRS4BaVWLMUnB1jLPT.d4BBZWl9RnXDAbPzIrMdrj8nvrj2lBu','أميرة مصطفى','01096325874','مدير',0,'2025-10-13 00:00:00');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-21 15:40:02
