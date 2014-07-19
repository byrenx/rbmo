-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: mysql.server    Database: byrenx$rbmo
-- ------------------------------------------------------
-- Server version	5.1.63-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `byrenx$rbmo`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `byrenx$rbmo` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `byrenx$rbmo`;

--
-- Table structure for table `agency`
--

DROP TABLE IF EXISTS `agency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `sector_id` int(11) NOT NULL,
  `email` varchar(75) NOT NULL,
  `acces_key` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `agency_94c48b8` (`sector_id`),
  CONSTRAINT `sector_id_refs_id_47930c10` FOREIGN KEY (`sector_id`) REFERENCES `sector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agency`
--

LOCK TABLES `agency` WRITE;
/*!40000 ALTER TABLE `agency` DISABLE KEYS */;
INSERT INTO `agency` VALUES (1,'TESDA',5,'tesda@gmail.com',''),(2,'Regional Budget and Management Office',6,'rbmo.armm@yahoo.com',''),(3,'Bureau on Cultural Heritage-ARMM',10,'bch.armm@yahoo.com',''),(4,'ARMM Development Academy',6,'ada.armm@yahho.com',''),(5,'Civil Aviation Authority of the Philippines',9,'DOTC@yahoo.com',''),(6,'Office for Southern Cultural Communities',6,'OSCC@yahoo.com',''),(7,'Housing and Land Use Regulatory Board',10,'HLURB@yahoo.com',''),(8,'Department of Science and Technology-ARMM',5,'DOST@yahoo.com',''),(9,'Cooperative Development Authority',6,'CDA@yahoo.com',''),(10,'Coordinating and Development Office on Bangsamoro Youth Affairs',6,'CDOBYA@yahoo.com',''),(11,'REZA-Polloc Freeport',10,'RPF@yahoo.com',''),(12,'Office of the Regional Governor',3,'ORG@yahoo.com',''),(13,'Administration of the Blue Mosque',3,'ABM@yahoo.com',''),(14,'Office of the Deputy Governors',3,'ODG@yahoo.com',''),(15,'Office of the Executive Secretary',3,'OESec@yahoo.com',''),(16,'Office of the Cabinet Secretary',3,'CabSec@yahoo.com',''),(17,'Office of the Chief Staff',3,'ChiefStaff@yahoo.com',''),(18,'Administrative Management Service',3,'AMS@yahoo.com',''),(19,'Finance and Budget Management Services',3,'FBMS@yahoo.com',''),(20,'Intelligence Security Services',3,'ISS@yahoo.com','');
/*!40000 ALTER TABLE `agency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `allotmentreleases`
--

DROP TABLE IF EXISTS `allotmentreleases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `allotmentreleases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `agency_id` int(11) NOT NULL,
  `allocation` varchar(4) NOT NULL,
  `ada_no` varchar(5) NOT NULL,
  `date_release` date NOT NULL,
  `month` int(11) NOT NULL,
  `amount_release` decimal(15,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `allotmentreleases_b162e9d` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_12b7d33b` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `allotmentreleases`
--

LOCK TABLES `allotmentreleases` WRITE;
/*!40000 ALTER TABLE `allotmentreleases` DISABLE KEYS */;
/*!40000 ALTER TABLE `allotmentreleases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_9af0b65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add message',5,'add_message'),(14,'Can change message',5,'change_message'),(15,'Can delete message',5,'delete_message'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add permissions',8,'add_permissions'),(23,'Can change permissions',8,'change_permissions'),(24,'Can delete permissions',8,'delete_permissions'),(25,'Can add groups',9,'add_groups'),(26,'Can change groups',9,'change_groups'),(27,'Can delete groups',9,'delete_groups'),(28,'Can add group permissions',10,'add_grouppermissions'),(29,'Can change group permissions',10,'change_grouppermissions'),(30,'Can delete group permissions',10,'delete_grouppermissions'),(31,'Can add user group',11,'add_usergroup'),(32,'Can change user group',11,'change_usergroup'),(33,'Can delete user group',11,'delete_usergroup'),(34,'Can add user activity',12,'add_useractivity'),(35,'Can change user activity',12,'change_useractivity'),(36,'Can delete user activity',12,'delete_useractivity'),(37,'Can add sector',13,'add_sector'),(38,'Can change sector',13,'change_sector'),(39,'Can delete sector',13,'delete_sector'),(40,'Can add agency',14,'add_agency'),(41,'Can change agency',14,'change_agency'),(42,'Can delete agency',14,'delete_agency'),(43,'Can add notification',15,'add_notification'),(44,'Can change notification',15,'change_notification'),(45,'Can delete notification',15,'delete_notification'),(46,'Can add cos submission',16,'add_cossubmission'),(47,'Can change cos submission',16,'change_cossubmission'),(48,'Can delete cos submission',16,'delete_cossubmission'),(49,'Can add budget proposal',17,'add_budgetproposal'),(50,'Can change budget proposal',17,'change_budgetproposal'),(51,'Can delete budget proposal',17,'delete_budgetproposal'),(52,'Enter data from WFP',17,'record_wfp'),(53,'Print Agency WFP Information',17,'print_report'),(54,'Can add wfp data',18,'add_wfpdata'),(55,'Can change wfp data',18,'change_wfpdata'),(56,'Can delete wfp data',18,'delete_wfpdata'),(57,'Enter data from WFP',18,'record_wfp'),(58,'Print Agency WFP Information',18,'print_report'),(59,'Can add performance target',19,'add_performancetarget'),(60,'Can change performance target',19,'change_performancetarget'),(61,'Can delete performance target',19,'delete_performancetarget'),(62,'Can add allotment releases',20,'add_allotmentreleases'),(63,'Can change allotment releases',20,'change_allotmentreleases'),(64,'Can delete allotment releases',20,'delete_allotmentreleases'),(65,'Can add mpfro',21,'add_mpfro'),(66,'Can change mpfro',21,'change_mpfro'),(67,'Can delete mpfro',21,'delete_mpfro'),(68,'Can add mpfro accomplishment',22,'add_mpfroaccomplishment'),(69,'Can change mpfro accomplishment',22,'change_mpfroaccomplishment'),(70,'Can delete mpfro accomplishment',22,'delete_mpfroaccomplishment'),(71,'Can add wfp submission',23,'add_wfpsubmission'),(72,'Can change wfp submission',23,'change_wfpsubmission'),(73,'Can delete wfp submission',23,'delete_wfpsubmission'),(74,'Can add fund balances',24,'add_fundbalances'),(75,'Can change fund balances',24,'change_fundbalances'),(76,'Can delete fund balances',24,'delete_fundbalances'),(77,'Can add mpfr submission',25,'add_mpfrsubmission'),(78,'Can change mpfr submission',25,'change_mpfrsubmission'),(79,'Can delete mpfr submission',25,'delete_mpfrsubmission'),(80,'Can add quarterly req',26,'add_quarterlyreq'),(81,'Can change quarterly req',26,'change_quarterlyreq'),(82,'Can delete quarterly req',26,'delete_quarterlyreq'),(83,'Can add quarter req submission',27,'add_quarterreqsubmission'),(84,'Can change quarter req submission',27,'change_quarterreqsubmission'),(85,'Can delete quarter req submission',27,'delete_quarterreqsubmission'),(86,'Can add co request',28,'add_corequest'),(87,'Can change co request',28,'change_corequest'),(88,'Can delete co request',28,'delete_corequest');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'byrenx@gmail.com','Jofel','Bayron','byrenx@gmail.com','pbkdf2_sha256$12000$RUq1qJjeOnTJ$Pg/flPPiPH/Vzb90FD1ewLqsHnrXXAJVJEZGRXhqKO0=',1,1,1,'2014-07-12 06:23:00','2014-07-12 01:47:07'),(2,'rumzster@gmail.com','Rommel','Asibal','rumzster@gmail.com','pbkdf2_sha256$12000$dRrtHIaP4hLC$Pqi2r3TfURAIw62QqBvGQJPJ3/RFPYe/BZ8Ru8cKeik=',0,1,0,'2014-07-16 05:01:09','2014-07-12 06:23:43'),(3,'sittie@gmail.com','Sittie','Bantayao','sittie@gmail.com','pbkdf2_sha256$12000$VmBFtEjIS5bf$7K3kFr8PRL6+50COmZdZBBHvLXJe2He7CPnciurXqW0=',0,1,0,'2014-07-17 00:33:05','2014-07-12 07:09:34'),(4,'jessielibita.jcl@gmail.com','Jessie','Libita','jessielibita.jcl@gmail.com','pbkdf2_sha256$12000$wuQkIkDlRuvM$2bndJKBguLUgKrzypKVpDUJ7IC9UcrMjhNNVlpzR0Ms=',0,1,0,'2014-07-17 03:05:15','2014-07-12 07:11:43'),(5,'helmiesalendab@gmail.com','helmie','salendab','helmiesalendab@gmail.com','pbkdf2_sha256$12000$k1RqU2onDRMg$JZKr2nLjF7LHW8fdp1NZ54Qa4xoPk20UYtzfgzyfmXA=',0,1,0,'2014-07-16 05:43:03','2014-07-16 03:15:23'),(6,'test@gmail.com','test','Test','test@gmail.com','pbkdf2_sha256$12000$LjzcA2d3KUs1$WBUUuKXolxcw13ELVsCE3SSXF2FhglSnRrynwne5VXY=',0,1,0,'2014-07-16 03:32:36','2014-07-16 03:32:26'),(8,'helmie_salendab@gmail.com','Helmie','Salendab','helmie_salendab@gmail.com','pbkdf2_sha256$12000$qg3NKad82gLA$mRK5cGlhZowTjh8uBi210FfldiKUio8oOT6AjcnUIKg=',0,1,0,'2014-07-16 05:41:16','2014-07-16 05:41:16');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `budget_proposal`
--

DROP TABLE IF EXISTS `budget_proposal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `budget_proposal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `activity` varchar(200) NOT NULL,
  `agency_id` int(11) NOT NULL,
  `allocation` varchar(4) NOT NULL,
  `performance_indicator` varchar(45) NOT NULL,
  `q1` int(11) NOT NULL,
  `q2` int(11) NOT NULL,
  `q3` int(11) NOT NULL,
  `q4` int(11) NOT NULL,
  `jan` decimal(12,2) NOT NULL,
  `feb` decimal(12,2) NOT NULL,
  `mar` decimal(12,2) NOT NULL,
  `apr` decimal(12,2) NOT NULL,
  `may` decimal(12,2) NOT NULL,
  `jun` decimal(12,2) NOT NULL,
  `jul` decimal(12,2) NOT NULL,
  `aug` decimal(12,2) NOT NULL,
  `sept` decimal(12,2) NOT NULL,
  `oct` decimal(12,2) NOT NULL,
  `nov` decimal(12,2) NOT NULL,
  `dec` decimal(12,2) NOT NULL,
  `total` decimal(15,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `budget_proposal_b162e9d` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_1793bcdf` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budget_proposal`
--

LOCK TABLES `budget_proposal` WRITE;
/*!40000 ALTER TABLE `budget_proposal` DISABLE KEYS */;
/*!40000 ALTER TABLE `budget_proposal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `co_request`
--

DROP TABLE IF EXISTS `co_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `co_request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_received` date NOT NULL,
  `agency_id` int(11) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `action` varchar(100) NOT NULL,
  `status` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `co_request_b162e9d` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_8d656384` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `co_request`
--

LOCK TABLES `co_request` WRITE;
/*!40000 ALTER TABLE `co_request` DISABLE KEYS */;
INSERT INTO `co_request` VALUES (1,'2014-12-12',2,'Request for release of Capital of RBMO','Transmitted to ORT for release','okay'),(2,'2014-07-14',2,'Request for release of PS for the month of July','Transmitted to ORT for release','Okay'),(3,'2014-07-16',3,'Request for realignment','Forwarded to ED','Pending for Approval');
/*!40000 ALTER TABLE `co_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cos_submission`
--

DROP TABLE IF EXISTS `cos_submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cos_submission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_id` int(11) NOT NULL,
  `date_submitted` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cos_submission_b162e9d` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_976c2968` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cos_submission`
--

LOCK TABLES `cos_submission` WRITE;
/*!40000 ALTER TABLE `cos_submission` DISABLE KEYS */;
INSERT INTO `cos_submission` VALUES (1,2,'2014-07-14 01:47:26'),(2,2,'2014-07-15 08:59:45'),(3,3,'2014-07-16 03:49:49'),(4,5,'2014-07-16 06:34:56'),(5,4,'2014-07-16 08:46:12');
/*!40000 ALTER TABLE `cos_submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'message','auth','message'),(6,'content type','contenttypes','contenttype'),(7,'session','sessions','session'),(8,'permissions','rbmo','permissions'),(9,'groups','rbmo','groups'),(10,'group permissions','rbmo','grouppermissions'),(11,'user group','rbmo','usergroup'),(12,'user activity','rbmo','useractivity'),(13,'sector','rbmo','sector'),(14,'agency','rbmo','agency'),(15,'notification','rbmo','notification'),(16,'cos submission','rbmo','cossubmission'),(17,'budget proposal','rbmo','budgetproposal'),(18,'wfp data','rbmo','wfpdata'),(19,'performance target','rbmo','performancetarget'),(20,'allotment releases','rbmo','allotmentreleases'),(21,'mpfro','rbmo','mpfro'),(22,'mpfro accomplishment','rbmo','mpfroaccomplishment'),(23,'wfp submission','rbmo','wfpsubmission'),(24,'fund balances','rbmo','fundbalances'),(25,'mpfr submission','rbmo','mpfrsubmission'),(26,'quarterly req','rbmo','quarterlyreq'),(27,'quarter req submission','rbmo','quarterreqsubmission'),(28,'co request','rbmo','corequest');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0rv0qw8543a5aybjpsz0ldyzq28pj5fi','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-31 00:33:05'),('2rcoywjk1cry63b58xrqrzr24vljzqpr','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-28 13:07:05'),('5hkqh3gumpv0n8usnzme2r03maadmy2r','MmY0MDc3ODE2YWEwMzZjOTIwNjA1OThmMjNiODY1NzM1NTFmMTIyZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NH0=','2014-07-30 05:39:41'),('75uh9ddlaxcj31l65w1y8fbs09cwmsfn','YWViYTAwOTljOTM3NDQ1YmU4MzMyODI5Y2M3M2Y3Y2RlOTZiODYwZTp7Il9hdXRoX3VzZXJfaWQiOjIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2014-07-28 01:41:03'),('aul8d35nxe3veypefdv3ct9gwxd1i2q2','MmY0MDc3ODE2YWEwMzZjOTIwNjA1OThmMjNiODY1NzM1NTFmMTIyZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NH0=','2014-07-31 03:05:15'),('axfsf5mdx3vf7ll4klwf2ltzidntzq3g','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-29 08:54:15'),('b99gs74f63a0u9ueaqtrkk64xwwnzwew','OTI4YTIyYWM5YWY4MzBmMWRkZjc2YTRlZTgzNTJmNzY5NmM2NDkxMTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2014-07-26 06:24:12'),('bm0cejjbs7djajqmc6ehju6fkduha257','MDE4OTlmM2I3ZDBkOWY5N2UzM2QwMDc4MzUwNmM0MmEyNTU5ZTcwNTp7fQ==','2014-07-26 06:53:07'),('cqb2h1zgbfvfb3iegyvmpmegswnek9lc','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-30 03:21:37'),('crzhcuxnodt9snxx8izh9ceg7edfvldi','MDE4OTlmM2I3ZDBkOWY5N2UzM2QwMDc4MzUwNmM0MmEyNTU5ZTcwNTp7fQ==','2014-08-01 01:52:36'),('hn85y2jh2zs7lqycct2xm4022bi21nhb','OTI4YTIyYWM5YWY4MzBmMWRkZjc2YTRlZTgzNTJmNzY5NmM2NDkxMTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2014-07-30 05:01:09'),('k9aoj6ke3wabcebm7os9ja7bxhrhn7t3','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-28 23:32:13'),('osep9s2ak6yxd1wkh13d28kz2s2893w3','MmY0MDc3ODE2YWEwMzZjOTIwNjA1OThmMjNiODY1NzM1NTFmMTIyZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NH0=','2014-07-29 09:25:03'),('p0q9534wqgup61wop8v8xbtnluxqvjlh','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-30 08:43:12'),('qqxobzyx9w7tkg0zyvi2yrafjs297tur','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-29 03:49:26'),('r3gn8m70j7u5dzqtxr96ttembg1nayqi','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-30 04:31:27'),('s4ad2r626cdt1977ytaxfgse9pw6n2px','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-30 03:20:59'),('v2r2riuif6v9otqfr2rxpkc2w1ax53cz','MmY0MDc3ODE2YWEwMzZjOTIwNjA1OThmMjNiODY1NzM1NTFmMTIyZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NH0=','2014-07-29 08:58:26'),('vpl55anfp7crf2wcu7n1ds5tvhok9klj','MmY0MDc3ODE2YWEwMzZjOTIwNjA1OThmMjNiODY1NzM1NTFmMTIyZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NH0=','2014-07-28 05:05:54'),('xjg0fxusxvmo6liw6vfblqjyh7gviam9','MmU1NmNlYjU0YTFjYjk2MGRjNTg0MGNmM2U4ODZjZWU3ZWFkMWRlOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6M30=','2014-07-28 01:35:25'),('zxg11mlcqi83dj157uybazloxn0oqlz9','MmY0MDc3ODE2YWEwMzZjOTIwNjA1OThmMjNiODY1NzM1NTFmMTIyZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NH0=','2014-07-30 06:00:49');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fund_balances`
--

DROP TABLE IF EXISTS `fund_balances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fund_balances` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `agency_id` int(11) NOT NULL,
  `ps` decimal(15,2) NOT NULL,
  `mooe` decimal(15,2) NOT NULL,
  `co` decimal(15,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fund_balances_b162e9d` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_329d71c4` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fund_balances`
--

LOCK TABLES `fund_balances` WRITE;
/*!40000 ALTER TABLE `fund_balances` DISABLE KEYS */;
/*!40000 ALTER TABLE `fund_balances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_perm`
--

DROP TABLE IF EXISTS `group_perm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_perm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `group_perm_bda51c3c` (`group_id`),
  KEY `group_perm_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_ee22793` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `permission_id_refs_id_1a7da3a2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_perm`
--

LOCK TABLES `group_perm` WRITE;
/*!40000 ALTER TABLE `group_perm` DISABLE KEYS */;
INSERT INTO `group_perm` VALUES (1,1,4),(2,1,5),(3,1,6),(4,1,11),(5,1,7),(6,1,15),(7,1,16),(8,1,17),(9,1,18),(10,1,19),(11,1,20),(12,1,21),(13,1,22),(14,1,23),(15,1,24),(16,1,27),(17,1,28),(18,2,4),(19,2,5),(20,2,8),(21,2,9),(22,2,10),(23,2,11),(24,2,12),(25,1,13),(26,1,14),(27,1,15),(28,1,16),(29,1,17),(30,1,18),(31,1,19),(32,1,20),(33,1,21),(34,1,22),(35,1,23),(36,1,24),(37,1,27),(38,1,28),(39,3,4),(40,3,5),(41,3,11),(42,3,27),(43,3,28),(44,3,29),(45,3,30),(46,4,1),(47,4,2),(48,4,3),(49,4,4),(50,4,5),(51,4,6),(52,4,7),(53,4,8),(54,4,9),(55,4,10),(56,4,11),(57,4,12),(58,4,13),(59,4,14),(60,4,15),(61,4,16),(62,4,17),(63,4,18),(64,4,19),(65,4,20),(66,4,21),(67,4,22),(68,4,23),(69,4,24),(70,4,25),(71,4,26),(72,4,27),(73,4,28),(74,4,29),(75,4,30),(76,4,31),(77,4,32),(78,4,33),(79,1,4),(80,1,5),(81,1,6),(82,1,11),(83,1,7),(84,1,15),(85,1,16),(86,1,17),(87,1,18),(88,1,19),(89,1,20),(90,1,21),(91,1,22),(92,1,23),(93,1,24),(94,1,27),(95,1,28),(96,2,4),(97,2,5),(98,2,8),(99,2,9),(100,2,10),(101,2,11),(102,2,12),(103,1,13),(104,1,14),(105,1,15),(106,1,16),(107,1,17),(108,1,18),(109,1,19),(110,1,20),(111,1,21),(112,1,22),(113,1,23),(114,1,24),(115,1,27),(116,1,28),(117,3,4),(118,3,5),(119,3,11),(120,3,27),(121,3,28),(122,3,29),(123,3,30),(124,4,1),(125,4,2),(126,4,3),(127,4,4),(128,4,5),(129,4,6),(130,4,7),(131,4,8),(132,4,9),(133,4,10),(134,4,11),(135,4,12),(136,4,13),(137,4,14),(138,4,15),(139,4,16),(140,4,17),(141,4,18),(142,4,19),(143,4,20),(144,4,21),(145,4,22),(146,4,23),(147,4,24),(148,4,25),(149,4,26),(150,4,27),(151,4,28),(152,4,29),(153,4,30),(154,4,31),(155,4,32),(156,4,33);
/*!40000 ALTER TABLE `group_perm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES (1,'Recording Officer'),(2,'BEAM'),(3,'BPAC'),(4,'Administrator');
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mpfr_submission`
--

DROP TABLE IF EXISTS `mpfr_submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mpfr_submission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `agency_id` int(11) NOT NULL,
  `jan` date DEFAULT NULL,
  `feb` date DEFAULT NULL,
  `mar` date DEFAULT NULL,
  `apr` date DEFAULT NULL,
  `may` date DEFAULT NULL,
  `jun` date DEFAULT NULL,
  `jul` date DEFAULT NULL,
  `aug` date DEFAULT NULL,
  `sept` date DEFAULT NULL,
  `oct` date DEFAULT NULL,
  `nov` date DEFAULT NULL,
  `dec` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mpfr_submission_b162e9d` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_7df5b881` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mpfr_submission`
--

LOCK TABLES `mpfr_submission` WRITE;
/*!40000 ALTER TABLE `mpfr_submission` DISABLE KEYS */;
INSERT INTO `mpfr_submission` VALUES (1,2014,2,'2014-07-14','2014-07-14','2014-07-14','2014-07-14','2014-07-14','2014-07-14','2014-07-15',NULL,NULL,NULL,NULL,NULL),(2,2014,5,'2014-07-16','2014-07-16','2014-07-16','2014-07-16','2014-07-16','2014-07-16',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `mpfr_submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mpfro`
--

DROP TABLE IF EXISTS `mpfro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mpfro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `activity_id` int(11) NOT NULL,
  `allot_receive` decimal(15,2) NOT NULL,
  `incurred` decimal(15,2) NOT NULL,
  `remaining` decimal(15,2) NOT NULL,
  `remarks` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `activity_id` (`activity_id`),
  KEY `mpfro_b162e9d` (`agency_id`),
  CONSTRAINT `activity_id_refs_id_633da3b4` FOREIGN KEY (`activity_id`) REFERENCES `wfp_data` (`id`),
  CONSTRAINT `agency_id_refs_id_45cb3735` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mpfro`
--

LOCK TABLES `mpfro` WRITE;
/*!40000 ALTER TABLE `mpfro` DISABLE KEYS */;
/*!40000 ALTER TABLE `mpfro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mpfro_acc`
--

DROP TABLE IF EXISTS `mpfro_acc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mpfro_acc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mpfro_id` int(11) NOT NULL,
  `p_target_id` int(11) NOT NULL,
  `target` int(11) NOT NULL,
  `accomplished` int(11) NOT NULL,
  `variance` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `p_target_id` (`p_target_id`),
  KEY `mpfro_acc_8d221593` (`mpfro_id`),
  CONSTRAINT `mpfro_id_refs_id_f18821db` FOREIGN KEY (`mpfro_id`) REFERENCES `mpfro` (`id`),
  CONSTRAINT `p_target_id_refs_id_7366e45a` FOREIGN KEY (`p_target_id`) REFERENCES `performancetarget` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mpfro_acc`
--

LOCK TABLES `mpfro_acc` WRITE;
/*!40000 ALTER TABLE `mpfro_acc` DISABLE KEYS */;
/*!40000 ALTER TABLE `mpfro_acc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_id` int(11) NOT NULL,
  `date_notify` date NOT NULL,
  `subject` varchar(45) NOT NULL,
  `msg` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notification_b162e9d` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_74da32b3` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `performancetarget`
--

DROP TABLE IF EXISTS `performancetarget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `performancetarget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wfp_activity_id` int(11) NOT NULL,
  `indicator` varchar(45) NOT NULL,
  `q1` int(11) NOT NULL,
  `q2` int(11) NOT NULL,
  `q3` int(11) NOT NULL,
  `q4` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `performancetarget_80547e07` (`wfp_activity_id`),
  CONSTRAINT `wfp_activity_id_refs_id_310df8e3` FOREIGN KEY (`wfp_activity_id`) REFERENCES `wfp_data` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `performancetarget`
--

LOCK TABLES `performancetarget` WRITE;
/*!40000 ALTER TABLE `performancetarget` DISABLE KEYS */;
INSERT INTO `performancetarget` VALUES (1,1,'No. of Employees paid',3,3,3,3),(2,2,'No. of Employees paid',6,6,6,6),(3,5,'No. of Employees Paid',26,26,26,26),(4,6,'No. Employees paid',12,12,12,12),(5,8,'No. of Employees Paid',2,2,1,1),(6,9,'No. of reports Submitted',6,6,6,6);
/*!40000 ALTER TABLE `performancetarget` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` varchar(10) NOT NULL,
  `target` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES (1,'add','agency'),(2,'edit','agency'),(3,'delete','agency'),(4,'view','agency information'),(5,'view','agency submitted documents'),(6,'add','agency submitted documents'),(7,'delete','agency submitted documents'),(8,'add','agency approved budget'),(9,'edit','agency approved budget'),(10,'delete','agency approved budget'),(11,'view','agency approved budget'),(12,'add','fund request'),(13,'edit','fund request'),(14,'delete','fund request'),(15,'view','running balances'),(16,'print','running balances'),(17,'view','status of allotment releases'),(18,'print','status of allotment releases'),(19,'view','total releases'),(20,'print','total releases'),(21,'view','monthly reports'),(22,'print','monthly reports'),(23,'view','quarterly report'),(24,'print','quarterly report'),(25,'view','transaction history'),(26,'delete','transaction history'),(27,'view','analysis report'),(28,'print','analysis report'),(29,'print','fund utilization'),(30,'view','fund utilization'),(31,'add','user'),(32,'edit','user'),(33,'view','user');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quarter_req_submit`
--

DROP TABLE IF EXISTS `quarter_req_submit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quarter_req_submit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_id` int(11) NOT NULL,
  `requirement_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `quarter` int(11) NOT NULL,
  `date_submitted` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quarter_req_submit_b162e9d` (`agency_id`),
  KEY `quarter_req_submit_99a85f32` (`requirement_id`),
  CONSTRAINT `agency_id_refs_id_bfdda89c` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`),
  CONSTRAINT `requirement_id_refs_id_61e17802` FOREIGN KEY (`requirement_id`) REFERENCES `quarterly_req` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quarter_req_submit`
--

LOCK TABLES `quarter_req_submit` WRITE;
/*!40000 ALTER TABLE `quarter_req_submit` DISABLE KEYS */;
INSERT INTO `quarter_req_submit` VALUES (1,2,1,2014,1,'2014-07-14'),(2,2,1,2014,2,'2014-07-14'),(3,2,2,2014,1,'2014-07-14'),(4,2,2,2014,2,'2014-07-14'),(5,2,3,2014,1,'2014-07-14'),(6,2,3,2014,2,'2014-07-14'),(7,2,4,2014,1,'2014-07-14'),(8,2,4,2014,2,'2014-07-14'),(9,2,1,2014,3,'2014-07-15'),(10,2,1,2014,4,'2014-07-15'),(11,3,1,2014,1,'2014-07-16'),(12,3,2,2014,1,'2014-07-16'),(13,3,3,2014,1,'2014-07-16'),(14,3,4,2014,1,'2014-07-16'),(15,5,1,2014,1,'2014-07-16'),(16,5,1,2014,2,'2014-07-16'),(17,5,2,2014,1,'2014-07-16'),(18,5,2,2014,2,'2014-07-16'),(19,5,3,2014,1,'2014-07-16'),(20,5,3,2014,2,'2014-07-16'),(21,5,4,2014,1,'2014-07-16'),(22,5,4,2014,2,'2014-07-16');
/*!40000 ALTER TABLE `quarter_req_submit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quarterly_req`
--

DROP TABLE IF EXISTS `quarterly_req`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quarterly_req` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quarterly_req`
--

LOCK TABLES `quarterly_req` WRITE;
/*!40000 ALTER TABLE `quarterly_req` DISABLE KEYS */;
INSERT INTO `quarterly_req` VALUES (1,'Statement of Allotment, Obligation and balances'),(2,'Status of Funds'),(3,'Reports of Detailed Disbursement'),(4,'Narrative Accomplishment Reports');
/*!40000 ALTER TABLE `quarterly_req` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sector`
--

DROP TABLE IF EXISTS `sector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sector` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sector`
--

LOCK TABLES `sector` WRITE;
/*!40000 ALTER TABLE `sector` DISABLE KEYS */;
INSERT INTO `sector` VALUES (1,'Environmental Conservation & Mgt & Human Settlement'),(2,'Regional Legislative Services'),(3,'Administrative & Financial management Services'),(4,'Health Services'),(5,'Education, Science & Technology'),(6,'Livelihood, Social Welfare and Protection Services'),(7,'Employment Promotion & Development & Industrial Peace'),(8,'Trade Industry & Investment Development'),(9,'Transportation & Communication Regulation Services'),(10,'Road Network, Public Infra & Other Development');
/*!40000 ALTER TABLE `sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_activity`
--

DROP TABLE IF EXISTS `user_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `action` varchar(100) NOT NULL,
  `act_date` datetime NOT NULL,
  `target` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_activity_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_a9a811e6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_activity`
--

LOCK TABLES `user_activity` WRITE;
/*!40000 ALTER TABLE `user_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_group`
--

DROP TABLE IF EXISTS `user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `user_group_bda51c3c` (`group_id`),
  CONSTRAINT `group_id_refs_id_ef60178a` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `user_id_refs_id_8bf36df` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_group`
--

LOCK TABLES `user_group` WRITE;
/*!40000 ALTER TABLE `user_group` DISABLE KEYS */;
INSERT INTO `user_group` VALUES (1,1,4),(2,2,4),(3,3,4),(4,4,4),(5,5,2),(6,6,4),(7,8,4);
/*!40000 ALTER TABLE `user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `user_permissions`
--

DROP TABLE IF EXISTS `user_permissions`;
/*!50001 DROP VIEW IF EXISTS `user_permissions`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `user_permissions` (
  `id` tinyint NOT NULL,
  `username` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `action` tinyint NOT NULL,
  `target` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wfp_data`
--

DROP TABLE IF EXISTS `wfp_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wfp_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `activity` varchar(200) NOT NULL,
  `agency_id` int(11) NOT NULL,
  `allocation` varchar(4) NOT NULL,
  `jan` decimal(12,2) NOT NULL,
  `feb` decimal(12,2) NOT NULL,
  `mar` decimal(12,2) NOT NULL,
  `apr` decimal(12,2) NOT NULL,
  `may` decimal(12,2) NOT NULL,
  `jun` decimal(12,2) NOT NULL,
  `jul` decimal(12,2) NOT NULL,
  `aug` decimal(12,2) NOT NULL,
  `sept` decimal(12,2) NOT NULL,
  `oct` decimal(12,2) NOT NULL,
  `nov` decimal(12,2) NOT NULL,
  `dec` decimal(12,2) NOT NULL,
  `total` decimal(15,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wfp_data_b162e9d` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_8cc7fa5e` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wfp_data`
--

LOCK TABLES `wfp_data` WRITE;
/*!40000 ALTER TABLE `wfp_data` DISABLE KEYS */;
INSERT INTO `wfp_data` VALUES (1,2014,'Salaries and Wages',1,'PS',1990.00,1990.00,1990.00,1990.00,1990.00,1990.00,1990.00,1990.00,1990.00,1990.00,1990.00,1990.00,23880.00),(2,2014,'Operating Services',1,'MOOE',1890.00,1890.00,1890.00,1890.00,1890.00,1890.00,1890.00,1890.00,1890.00,1890.00,1890.00,1890.00,22680.00),(3,2014,'budget release services',2,'MOOE',0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00),(4,2014,'General Management and Supervision',2,'MOOE',183700.00,183700.00,183700.00,183700.00,183700.00,183700.00,183700.00,183700.00,183700.00,183700.00,183700.00,183700.00,2204400.00),(5,2014,'Salaries/Wages',2,'PS',465015.00,465015.00,465015.00,465015.00,465015.00,465015.00,465015.00,465015.00,465015.00,465015.00,465015.00,465015.00,5580180.00),(6,2014,'Salaries and Wages',3,'PS',40981442.00,40981442.00,40981442.00,40981442.00,40981442.00,40981442.00,40981442.00,40981442.00,40981442.00,40981442.00,40981442.00,40981442.00,491777304.00),(7,2014,'Salaries/Wages',4,'PS',259742.00,259742.00,259742.00,259742.00,259742.00,259742.00,259742.00,259742.00,259742.00,259742.00,259742.00,259742.00,3116904.00),(8,2014,'Other Compensation ',4,'PS',35717.00,35717.00,35717.00,35717.00,35717.00,35717.00,35717.00,35717.00,35717.00,35717.00,35717.00,35717.00,428604.00),(9,2014,'General Administration and Support Services',2,'MOOE',139512.50,139512.50,139512.50,139512.50,139512.50,139512.50,139512.50,139512.50,139512.50,139512.50,139512.50,139512.50,1674150.00),(11,2014,'Personnel Services',4,'PS',0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00),(12,2014,'Salaries & Wages',5,'PS',64000.00,64000.00,64000.00,64000.00,64000.00,64000.00,64000.00,64000.00,64000.00,64000.00,64000.00,64000.00,768000.00),(14,2014,'Maintenance of land side in accordance SARPS/ICAO ',5,'MOOE',10000.00,5000.00,5000.00,0.00,5000.00,0.00,5000.00,0.00,5000.00,0.00,5000.00,0.00,40000.00),(16,2014,'Capacity Building',5,'MOOE',0.00,0.00,7000.00,0.00,0.00,7000.00,0.00,2000.00,5000.00,0.00,0.00,7000.00,28000.00),(17,2014,'Supervision, Coordination, and Monitoring',5,'MOOE',10000.00,5000.00,0.00,5000.00,5000.00,0.00,0.00,5000.00,5000.00,0.00,0.00,0.00,35000.00),(18,2014,'Program/Project/Activity',20,'MOOE',0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00),(19,2014,'Program/Project/Activity',20,'MOOE',175000.00,175000.00,175000.00,175000.00,175000.00,175000.00,175000.00,175000.00,175000.00,175000.00,175000.00,175000.00,2100000.00),(20,2014,'Finance and Budget Management Service',19,'MOOE',160000.00,160000.00,160000.00,160000.00,160000.00,160000.00,160000.00,160000.00,160000.00,160000.00,160000.00,160000.00,1920000.00),(21,2014,'Program/Project/Activity',18,'MOOE',166667.00,166667.00,166667.00,166667.00,166667.00,166667.00,166667.00,166667.00,166667.00,166667.00,166667.00,166667.00,2000004.00);
/*!40000 ALTER TABLE `wfp_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wfp_submission`
--

DROP TABLE IF EXISTS `wfp_submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wfp_submission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_submitted` datetime NOT NULL,
  `year` int(11) NOT NULL,
  `agency_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wfp_submission_b162e9d` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_16f0da60` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wfp_submission`
--

LOCK TABLES `wfp_submission` WRITE;
/*!40000 ALTER TABLE `wfp_submission` DISABLE KEYS */;
INSERT INTO `wfp_submission` VALUES (1,'2014-07-12 06:27:04',2014,1),(2,'2014-07-14 01:47:15',2014,2),(3,'2014-07-16 03:32:17',2014,3),(4,'2014-07-16 05:47:42',2014,4),(5,'2014-07-16 06:34:58',2014,5),(6,'2014-07-17 03:19:24',2014,20),(7,'2014-07-17 03:29:42',2014,19),(8,'2014-07-17 03:33:01',2014,18),(9,'2014-07-17 03:34:54',2014,17);
/*!40000 ALTER TABLE `wfp_submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Current Database: `byrenx$rbmo`
--

USE `byrenx$rbmo`;

--
-- Final view structure for view `user_permissions`
--

/*!50001 DROP TABLE IF EXISTS `user_permissions`*/;
/*!50001 DROP VIEW IF EXISTS `user_permissions`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`byrenx`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `user_permissions` AS select `auth_user`.`id` AS `id`,`auth_user`.`username` AS `username`,`groups`.`name` AS `name`,`permissions`.`action` AS `action`,`permissions`.`target` AS `target` from ((((`auth_user` join `user_group` on((`user_group`.`user_id` = `auth_user`.`id`))) join `groups` on((`groups`.`id` = `user_group`.`group_id`))) join `group_perm` on((`group_perm`.`group_id` = `groups`.`id`))) join `permissions` on((`permissions`.`id` = `group_perm`.`permission_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-07-19  5:21:54
