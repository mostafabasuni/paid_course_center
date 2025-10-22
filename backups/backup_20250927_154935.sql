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
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE,
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE,
  CONSTRAINT `attendance_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`) ON DELETE CASCADE,
  CONSTRAINT `attendance_ibfk_4` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (1,23,4,9,7,'2025-08-24','الأحد'),(2,16,4,9,1,'2025-08-24','الأحد'),(3,8,1,1,3,'2025-08-24','الأحد'),(5,23,5,11,7,'2025-08-28','الخميس'),(6,11,6,12,6,'2025-09-20','السبت'),(7,16,4,9,6,'2025-09-20','السبت'),(8,16,6,12,6,'2025-09-23','الثلاثاء'),(9,14,4,9,6,'2025-09-23','الثلاثاء');
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
  `teacher_id` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_course_fields` (`name`,`grade_id`,`teacher_id`),
  KEY `course_grade_id` (`grade_id`),
  KEY `course_teacher_id` (`teacher_id`) USING BTREE,
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`) ON DELETE CASCADE,
  CONSTRAINT `course_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'لغة عربية',1,1,500.00),(2,'لغة انجليزية',1,2,500.00),(3,'رياضيات',1,4,500.00),(4,'لغة عربية',6,9,900.00),(5,'لغة انجليزية',6,11,900.00),(6,'رياضيات',6,12,900.00),(7,'لغة عربية',3,1,500.00),(8,'لغة انجليزية',3,2,500.00),(9,'رياضيات',3,4,500.00),(10,'لغة عربية',7,9,900.00),(11,'لغة انجليزية',7,11,900.00),(13,'رياضيات',7,12,900.00);
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
  `attendance_count` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `enrollment_student_id` (`student_id`),
  KEY `enrollment_teacher_id` (`teacher_id`),
  KEY `enrollment_grade_id` (`grade_id`),
  KEY `enrollment_course_id` (`course_id`),
  KEY `enrollment_user_id` (`user_id`),
  CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE,
  CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`) ON DELETE CASCADE,
  CONSTRAINT `enrollment_ibfk_3` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`) ON DELETE CASCADE,
  CONSTRAINT `enrollment_ibfk_4` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE,
  CONSTRAINT `enrollment_ibfk_5` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollment`
--

LOCK TABLES `enrollment` WRITE;
/*!40000 ALTER TABLE `enrollment` DISABLE KEYS */;
INSERT INTO `enrollment` VALUES (1,4,1,1,1,'سبتمبر',250.00,1,0,4,1),(2,4,2,1,2,'سبتمبر',250.00,1,0,4,1),(3,4,4,1,3,'سبتمبر',250.00,1,0,4,1),(4,5,2,1,2,'سبتمبر',250.00,0,1,4,1),(5,5,4,1,3,'سبتمبر',250.00,0,1,4,1),(6,4,1,1,1,'أكتوبر',500.00,0,0,0,1),(7,4,2,1,2,'أكتوبر',500.00,0,0,0,1),(8,4,4,1,3,'أكتوبر',500.00,0,0,0,1),(9,5,4,1,3,'أكتوبر',500.00,0,0,0,1),(10,5,2,1,2,'أكتوبر',500.00,0,0,0,1),(11,8,2,3,8,'أكتوبر',500.00,0,0,0,1),(12,8,1,3,7,'أكتوبر',500.00,0,0,0,1),(13,11,9,6,4,'أكتوبر',900.00,0,0,0,1),(14,11,12,6,6,'أكتوبر',900.00,0,0,0,1),(15,11,9,6,4,'سبتمبر',450.00,0,1,4,1),(16,11,11,6,5,'سبتمبر',450.00,0,1,4,1),(17,11,12,6,6,'سبتمبر',450.00,0,1,4,1),(18,14,9,6,4,'سبتمبر',450.00,0,1,4,1),(19,14,11,6,5,'سبتمبر',450.00,0,1,4,1),(20,14,12,6,6,'سبتمبر',450.00,0,1,4,1),(21,15,11,6,5,'سبتمبر',900.00,0,0,0,1),(22,15,12,6,6,'سبتمبر',900.00,0,0,0,1),(23,16,9,6,4,'سبتمبر',900.00,0,0,0,1),(24,16,12,6,6,'سبتمبر',900.00,0,0,0,1);
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
  UNIQUE KEY `unique_grade_fields` (`name`,`level`,`term`,`academic_year`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grade`
--

LOCK TABLES `grade` WRITE;
/*!40000 ALTER TABLE `grade` DISABLE KEYS */;
INSERT INTO `grade` VALUES (1,'الأول','الإعدادية','الأول','2025/2026'),(3,'الثاني','الإعدادية','الأول','2025/2026'),(5,'الثالث','الإعدادية','الأول','2025/2026'),(6,'الأول','الثانوية','الأول','2025/2026'),(7,'الثاني','الثانوية','الأول','2025/2026'),(8,'الثالث','الثانوية','الأول','2025/2026');
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
  `paid_type` varchar(255) NOT NULL,
  `payment_date` date NOT NULL,
  `month` varchar(15) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_student_id` (`student_id`),
  KEY `payment_user_id` (`user_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE,
  CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,4,750.00,0.00,'نقدي','2025-09-19','سبتمبر',1),(2,5,300.00,0.00,'فيزا','2025-09-19','سبتمبر',1),(3,14,1000.00,0.00,'نقدي','2025-09-20','سبتمبر',1),(4,15,1800.00,0.00,'فيزا','2025-09-20','سبتمبر',1),(5,16,1800.00,0.00,'نقدي','2025-09-20','سبتمبر',1);
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
  CONSTRAINT `permission_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,1,1,1,1,1,1,1,1,1,1,1,1,1),(2,2,1,1,1,1,1,0,0,0,0,0,1,1),(3,4,1,1,0,0,0,0,1,1,1,0,0,0);
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
  `reg_date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  KEY `student_grade_id` (`grade_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (4,'اسامة محمد خالد','01036925841',1,1,'2025-08-01'),(5,'يوسف سيد احمد خليل','01103698527',1,1,'2025-08-01'),(8,'سمير ماجد عبد الله','01103254888',3,1,'2025-08-01'),(11,'خالد يوسف احمد','01200963258',6,1,'2025-08-02'),(14,'مجدي احمد خالد','01200369852',6,1,'2025-08-12'),(15,'ياسر جمال هاني','01103214568',6,1,'2025-08-12'),(16,'منى ابراهيم السيد','01500125478',6,1,'2025-08-12'),(17,'معاذ حامد غالي','01559874563',1,1,'2025-08-12'),(18,'علي سعد علي','01111365489',3,1,'2025-08-12'),(19,'سعد ياسين فرج','01008521479',7,1,'2025-08-14'),(20,'مها ابراهيم سعد','01000065483',7,1,'2025-08-14'),(21,'يحيى زكريا احمد','01555963584',1,1,'2025-08-15'),(22,'هيثم محمد السيد','01123695241',3,1,'2025-08-15'),(23,'علي مروان احمد','01000985365',7,1,'2025-08-15'),(24,'عارف مهدي','01000987452',1,1,'2025-08-16'),(25,'شريف سامي العدوي','01000032569',6,1,'2025-09-03'),(26,'هاني سعد احمد','01100045698',1,1,'2025-09-03'),(28,'حسين يسري محمد','01200852369',1,1,'2025-09-03');
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
  CONSTRAINT `studentmonthlyinvoice_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentmonthlyinvoice`
--

LOCK TABLES `studentmonthlyinvoice` WRITE;
/*!40000 ALTER TABLE `studentmonthlyinvoice` DISABLE KEYS */;
INSERT INTO `studentmonthlyinvoice` VALUES (1,4,'سبتمبر',750.00,750.00,0.00,3),(2,5,'سبتمبر',500.00,300.00,200.00,2),(3,4,'أكتوبر',1500.00,0.00,1500.00,3),(4,5,'أكتوبر',1000.00,0.00,1000.00,2),(5,8,'أكتوبر',1000.00,0.00,1000.00,2),(6,11,'أكتوبر',1800.00,0.00,1800.00,2),(7,11,'سبتمبر',1350.00,0.00,1350.00,3),(8,14,'سبتمبر',1350.00,1000.00,350.00,3),(9,15,'سبتمبر',1800.00,1800.00,0.00,2),(10,16,'سبتمبر',1800.00,1800.00,0.00,2);
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
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES (1,'خالد ابراهيم','01001234569','لغة عربية - اعدادي',60.00),(2,'محمد فتحي','01012365478','لغة انجليزية - اعدادي',60.00),(4,'جمال مجدي احمد','01112365498','رياضيات - اعدادي',60.00),(9,'سمير احمد ابراهيم','01296325847','لغة عربية - ثانوي',60.00),(11,'يوسف حسن احمد','01585236974','لغة انجليزية - ثانوي',60.00),(12,'عبد الله محمد حسن','01112365478','رياضيات - ثانوي',60.00);
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
  CONSTRAINT `teacheraccount_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`) ON DELETE CASCADE,
  CONSTRAINT `teacheraccount_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacheraccount`
--

LOCK TABLES `teacheraccount` WRITE;
/*!40000 ALTER TABLE `teacheraccount` DISABLE KEYS */;
INSERT INTO `teacheraccount` VALUES (1,1,150.00,'سبتمبر',1,1,'2025-09-22',1),(2,2,300.00,'سبتمبر',2,1,'2025-09-22',1),(3,4,300.00,'سبتمبر',2,1,'2025-09-22',1),(4,1,600.00,'أكتوبر',2,0,'2025-09-17',1),(5,2,900.00,'أكتوبر',3,0,'2025-09-17',1),(6,4,600.00,'أكتوبر',2,0,'2025-09-17',1),(7,9,540.00,'أكتوبر',1,0,'2025-09-17',1),(8,12,540.00,'أكتوبر',1,0,'2025-09-17',1),(9,9,1080.00,'سبتمبر',3,0,'2025-09-19',1),(10,11,1080.00,'سبتمبر',3,0,'2025-09-19',1),(11,12,1620.00,'سبتمبر',4,0,'2025-09-19',1);
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
  CONSTRAINT `teachercourse_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`) ON DELETE CASCADE,
  CONSTRAINT `teachercourse_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE
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
  CONSTRAINT `teacherstudent_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`) ON DELETE CASCADE,
  CONSTRAINT `teacherstudent_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `teacherstudent_ibfk_3` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacherstudent`
--

LOCK TABLES `teacherstudent` WRITE;
/*!40000 ALTER TABLE `teacherstudent` DISABLE KEYS */;
INSERT INTO `teacherstudent` VALUES (1,1,4,1,'سبتمبر'),(2,2,4,1,'سبتمبر'),(3,4,4,1,'سبتمبر'),(4,2,5,1,'سبتمبر'),(5,4,5,1,'سبتمبر'),(6,1,4,1,'أكتوبر'),(7,2,4,1,'أكتوبر'),(8,4,4,1,'أكتوبر'),(9,4,5,1,'أكتوبر'),(10,2,5,1,'أكتوبر'),(11,2,8,3,'أكتوبر'),(12,1,8,3,'أكتوبر'),(13,9,11,6,'أكتوبر'),(14,12,11,6,'أكتوبر'),(15,9,11,6,'سبتمبر'),(16,11,11,6,'سبتمبر'),(17,12,11,6,'سبتمبر'),(18,9,14,6,'سبتمبر'),(19,11,14,6,'سبتمبر'),(20,12,14,6,'سبتمبر'),(21,11,15,6,'سبتمبر'),(22,12,15,6,'سبتمبر'),(23,9,16,6,'سبتمبر'),(24,12,16,6,'سبتمبر');
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
  `phone` varchar(20) NOT NULL,
  `job` varchar(50) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_username` (`username`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'mostafa','$2b$12$7eSlugqaRiavDFJQxSyTHel3Oqv4MLrfYpPxaKqnadOdz2VJho6A.','مصطفى بسيوني','01099231700','المدير العام',1,'2025-07-25 00:00:00'),(2,'amera','$2b$12$xgy5OIT9gI5X0MQomOkbb.r14qqV7NEoSbeML3zS2WgP7iY0qwP9W','أميرة مصطفى','01098745632','مدير',0,'2025-07-25 00:00:00'),(4,'eman','$2b$12$JUO.XxW3N2S/n/z0W/Mj8eqsC.Da8Qro4kb6EQy8Gs.2P.Yt.L1Y6','إيمان مصطفى','01009632587','مدير',0,'2025-07-26 00:00:00');
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

-- Dump completed on 2025-09-27 15:49:35
