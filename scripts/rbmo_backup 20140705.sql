-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.5.8


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema rbmo
--

CREATE DATABASE IF NOT EXISTS rbmo;
USE rbmo;

--
-- Temporary table structure for view `user_permissions`
--
DROP TABLE IF EXISTS `user_permissions`;
DROP VIEW IF EXISTS `user_permissions`;
CREATE TABLE `user_permissions` (
  `id` int(11),
  `username` varchar(30),
  `name` varchar(45),
  `action` varchar(10),
  `target` varchar(45)
);

--
-- Definition of table `agency`
--

DROP TABLE IF EXISTS `agency`;
CREATE TABLE `agency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `sector_id` int(11) NOT NULL,
  `email` varchar(75) NOT NULL,
  `acces_key` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `agency_663ed8c9` (`sector_id`),
  CONSTRAINT `sector_id_refs_id_312c8c48` FOREIGN KEY (`sector_id`) REFERENCES `sector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `agency`
--

/*!40000 ALTER TABLE `agency` DISABLE KEYS */;
INSERT INTO `agency` (`id`,`name`,`sector_id`,`email`,`acces_key`) VALUES 
 (1,'Department of Public Works and Highways',10,'dpwh@gmail.com','1234'),
 (2,'Department of Education',5,'deped@gmail.com','1234');
/*!40000 ALTER TABLE `agency` ENABLE KEYS */;


--
-- Definition of table `allocation`
--

DROP TABLE IF EXISTS `allocation`;
CREATE TABLE `allocation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `allocation`
--

/*!40000 ALTER TABLE `allocation` DISABLE KEYS */;
/*!40000 ALTER TABLE `allocation` ENABLE KEYS */;


--
-- Definition of table `allotmentreleases`
--

DROP TABLE IF EXISTS `allotmentreleases`;
CREATE TABLE `allotmentreleases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `allocation` varchar(4) NOT NULL,
  `ada_no` varchar(5) NOT NULL,
  `date_release` date NOT NULL,
  `month` int(11) NOT NULL,
  `amount_release` decimal(15,2) NOT NULL,
  `agency_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_allotmentreleases_1` (`agency_id`),
  CONSTRAINT `FK_allotmentreleases_1` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `allotmentreleases`
--

/*!40000 ALTER TABLE `allotmentreleases` DISABLE KEYS */;
INSERT INTO `allotmentreleases` (`id`,`year`,`allocation`,`ada_no`,`date_release`,`month`,`amount_release`,`agency_id`) VALUES 
 (5,2014,'PS','19','2014-07-05',1,'92728.00',1),
 (6,2014,'MOOE','3','2014-07-05',1,'200000.00',1),
 (7,2014,'MOOE','28','2014-07-05',1,'848503.00',1),
 (8,2014,'PS','48','2014-07-05',1,'416960.00',1),
 (11,2014,'PS','110','2014-07-05',2,'579800.00',1),
 (12,2014,'MOOE','98','2014-07-05',2,'603793.00',1),
 (13,2014,'PS','154','2014-07-05',3,'597800.00',1),
 (14,2014,'MOOE','193','2014-07-05',3,'678943.00',1),
 (15,2014,'PS','223','2014-07-05',4,'624800.00',1),
 (16,2014,'MOOE','263','2014-07-05',4,'702798.00',1);
/*!40000 ALTER TABLE `allotmentreleases` ENABLE KEYS */;


--
-- Definition of table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_group`
--

/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;


--
-- Definition of table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_group_permissions`
--

/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;


--
-- Definition of table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_permission`
--

/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` (`id`,`name`,`content_type_id`,`codename`) VALUES 
 (1,'Can add log entry',1,'add_logentry'),
 (2,'Can change log entry',1,'change_logentry'),
 (3,'Can delete log entry',1,'delete_logentry'),
 (4,'Can add permission',2,'add_permission'),
 (5,'Can change permission',2,'change_permission'),
 (6,'Can delete permission',2,'delete_permission'),
 (7,'Can add group',3,'add_group'),
 (8,'Can change group',3,'change_group'),
 (9,'Can delete group',3,'delete_group'),
 (10,'Can add user',4,'add_user'),
 (11,'Can change user',4,'change_user'),
 (12,'Can delete user',4,'delete_user'),
 (13,'Can add content type',5,'add_contenttype'),
 (14,'Can change content type',5,'change_contenttype'),
 (15,'Can delete content type',5,'delete_contenttype'),
 (16,'Can add session',6,'add_session'),
 (17,'Can change session',6,'change_session'),
 (18,'Can delete session',6,'delete_session'),
 (19,'Can add permissions',7,'add_permissions'),
 (20,'Can change permissions',7,'change_permissions'),
 (21,'Can delete permissions',7,'delete_permissions'),
 (22,'Can add groups',8,'add_groups'),
 (23,'Can change groups',8,'change_groups'),
 (24,'Can delete groups',8,'delete_groups'),
 (25,'Can add group permissions',9,'add_grouppermissions'),
 (26,'Can change group permissions',9,'change_grouppermissions'),
 (27,'Can delete group permissions',9,'delete_grouppermissions'),
 (28,'Can add user group',10,'add_usergroup'),
 (29,'Can change user group',10,'change_usergroup'),
 (30,'Can delete user group',10,'delete_usergroup'),
 (31,'Can add user activity',11,'add_useractivity'),
 (32,'Can change user activity',11,'change_useractivity'),
 (33,'Can delete user activity',11,'delete_useractivity'),
 (34,'Can add sector',12,'add_sector'),
 (35,'Can change sector',12,'change_sector'),
 (36,'Can delete sector',12,'delete_sector'),
 (37,'Can add agency',13,'add_agency'),
 (38,'Can change agency',13,'change_agency'),
 (39,'Can delete agency',13,'delete_agency'),
 (40,'Can add allocation',14,'add_allocation'),
 (41,'Can change allocation',14,'change_allocation'),
 (42,'Can delete allocation',14,'delete_allocation'),
 (43,'Can add budget proposal',15,'add_budgetproposal'),
 (44,'Can change budget proposal',15,'change_budgetproposal'),
 (45,'Can delete budget proposal',15,'delete_budgetproposal'),
 (46,'Enter data from WFP',15,'record_wfp'),
 (47,'Print Agency WFP Information',15,'print_report'),
 (48,'Can add wfp data',16,'add_wfpdata'),
 (49,'Can change wfp data',16,'change_wfpdata'),
 (50,'Can delete wfp data',16,'delete_wfpdata'),
 (51,'Enter data from WFP',16,'record_wfp'),
 (52,'Print Agency WFP Information',16,'print_report'),
 (53,'Can add performance target',17,'add_performancetarget'),
 (54,'Can change performance target',17,'change_performancetarget'),
 (55,'Can delete performance target',17,'delete_performancetarget'),
 (56,'Can add allotment releases',18,'add_allotmentreleases'),
 (57,'Can change allotment releases',18,'change_allotmentreleases'),
 (58,'Can delete allotment releases',18,'delete_allotmentreleases'),
 (59,'Can add mpfro',19,'add_mpfro'),
 (60,'Can change mpfro',19,'change_mpfro'),
 (61,'Can delete mpfro',19,'delete_mpfro'),
 (62,'Can add mpfro accomplishment',20,'add_mpfroaccomplishment'),
 (63,'Can change mpfro accomplishment',20,'change_mpfroaccomplishment'),
 (64,'Can delete mpfro accomplishment',20,'delete_mpfroaccomplishment'),
 (65,'Can add wfp submission',21,'add_wfpsubmission'),
 (66,'Can change wfp submission',21,'change_wfpsubmission'),
 (67,'Can delete wfp submission',21,'delete_wfpsubmission'),
 (68,'Can add fund balances',22,'add_fundbalances'),
 (69,'Can change fund balances',22,'change_fundbalances'),
 (70,'Can delete fund balances',22,'delete_fundbalances'),
 (71,'Can add mpfr submission',23,'add_mpfrsubmission'),
 (72,'Can change mpfr submission',23,'change_mpfrsubmission'),
 (73,'Can delete mpfr submission',23,'delete_mpfrsubmission'),
 (74,'Can add quarterly req',24,'add_quarterlyreq'),
 (75,'Can change quarterly req',24,'change_quarterlyreq'),
 (76,'Can delete quarterly req',24,'delete_quarterlyreq'),
 (77,'Can add quarter req submission',25,'add_quarterreqsubmission'),
 (78,'Can change quarter req submission',25,'change_quarterreqsubmission'),
 (79,'Can delete quarter req submission',25,'delete_quarterreqsubmission');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;


--
-- Definition of table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_user`
--

/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` (`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`) VALUES 
 (1,'pbkdf2_sha256$12000$pMOODsdxQhIT$GvQzrxRBCVluU3SJp3A/WR6xBoBBoKEVmPU7ExCy/t0=','2014-07-05 04:49:15',1,'byrenx@gmail.com','Jofel','Bayron','byrenx@gmail.com',1,1,'2014-07-04 06:24:52');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;


--
-- Definition of table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_user_groups`
--

/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;


--
-- Definition of table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_user_user_permissions`
--

/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;


--
-- Definition of table `budget_proposal`
--

DROP TABLE IF EXISTS `budget_proposal`;
CREATE TABLE `budget_proposal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `activity` varchar(200) NOT NULL,
  `agency_id` int(11) NOT NULL,
  `allocation_id` int(11) NOT NULL,
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
  KEY `budget_proposal_7bdfbc04` (`agency_id`),
  KEY `budget_proposal_427ae6a3` (`allocation_id`),
  CONSTRAINT `agency_id_refs_id_b2ab4eec` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`),
  CONSTRAINT `allocation_id_refs_id_4e7d10a7` FOREIGN KEY (`allocation_id`) REFERENCES `allocation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `budget_proposal`
--

/*!40000 ALTER TABLE `budget_proposal` DISABLE KEYS */;
/*!40000 ALTER TABLE `budget_proposal` ENABLE KEYS */;


--
-- Definition of table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
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
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_admin_log`
--

/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;


--
-- Definition of table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_content_type`
--

/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` (`id`,`name`,`app_label`,`model`) VALUES 
 (1,'log entry','admin','logentry'),
 (2,'permission','auth','permission'),
 (3,'group','auth','group'),
 (4,'user','auth','user'),
 (5,'content type','contenttypes','contenttype'),
 (6,'session','sessions','session'),
 (7,'permissions','rbmo','permissions'),
 (8,'groups','rbmo','groups'),
 (9,'group permissions','rbmo','grouppermissions'),
 (10,'user group','rbmo','usergroup'),
 (11,'user activity','rbmo','useractivity'),
 (12,'sector','rbmo','sector'),
 (13,'agency','rbmo','agency'),
 (14,'allocation','rbmo','allocation'),
 (15,'budget proposal','rbmo','budgetproposal'),
 (16,'wfp data','rbmo','wfpdata'),
 (17,'performance target','rbmo','performancetarget'),
 (18,'allotment releases','rbmo','allotmentreleases'),
 (19,'mpfro','rbmo','mpfro'),
 (20,'mpfro accomplishment','rbmo','mpfroaccomplishment'),
 (21,'wfp submission','rbmo','wfpsubmission'),
 (22,'fund balances','rbmo','fundbalances'),
 (23,'mpfr submission','rbmo','mpfrsubmission'),
 (24,'quarterly req','rbmo','quarterlyreq'),
 (25,'quarter req submission','rbmo','quarterreqsubmission');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;


--
-- Definition of table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` (`session_key`,`session_data`,`expire_date`) VALUES 
 ('3yv0wzgldj3yu419amvpac3m8itksm6t','M2JjZWE3MGM1N2U0MmE2ZDJmMDQ0NGQ5NWUyNDI3ZTYzY2Y4ZjJjOTp7IkFnZW50VXNlciI6MSwiYWdlbmN5X2lkIjoxfQ==','2014-07-19 08:10:46'),
 ('4m38chy4qg7xz3g96dz1dl9otuy2p9v2','ZDNkOWRlZWY3Y2IyOWI4OTJiNWE1M2QyOWRmODY2MDFkMThlMTcyZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-07-18 06:25:37'),
 ('b2uao62e28fb037m94td2pps4jupfkiv','ZDNkOWRlZWY3Y2IyOWI4OTJiNWE1M2QyOWRmODY2MDFkMThlMTcyZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-07-19 00:59:18'),
 ('m8oepht3ean27idqz9lmiix2hlx1889b','ZDNkOWRlZWY3Y2IyOWI4OTJiNWE1M2QyOWRmODY2MDFkMThlMTcyZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-07-18 08:53:59'),
 ('xh43gip5f2nhc30ne3pyvatmdk7sxbtf','ZDNkOWRlZWY3Y2IyOWI4OTJiNWE1M2QyOWRmODY2MDFkMThlMTcyZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-07-19 04:49:15'),
 ('zdwg5by0izjovelc4zpe9z7dvyfi2cws','ZDNkOWRlZWY3Y2IyOWI4OTJiNWE1M2QyOWRmODY2MDFkMThlMTcyZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-07-19 00:10:09');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;


--
-- Definition of table `fund_balances`
--

DROP TABLE IF EXISTS `fund_balances`;
CREATE TABLE `fund_balances` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `agency_id` int(11) NOT NULL,
  `ps` decimal(15,2) NOT NULL,
  `mooe` decimal(15,2) NOT NULL,
  `co` decimal(15,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fund_balances_7bdfbc04` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_00a1a53d` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fund_balances`
--

/*!40000 ALTER TABLE `fund_balances` DISABLE KEYS */;
/*!40000 ALTER TABLE `fund_balances` ENABLE KEYS */;


--
-- Definition of table `group_perm`
--

DROP TABLE IF EXISTS `group_perm`;
CREATE TABLE `group_perm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `group_perm_5f412f9a` (`group_id`),
  KEY `group_perm_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_491152f7` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `permission_id_refs_id_7d17467a` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `group_perm`
--

/*!40000 ALTER TABLE `group_perm` DISABLE KEYS */;
INSERT INTO `group_perm` (`id`,`group_id`,`permission_id`) VALUES 
 (1,1,4),
 (2,1,5),
 (3,1,6),
 (4,1,11),
 (5,1,7),
 (6,1,15),
 (7,1,16),
 (8,1,17),
 (9,1,18),
 (10,1,19),
 (11,1,20),
 (12,1,21),
 (13,1,22),
 (14,1,23),
 (15,1,24),
 (16,1,27),
 (17,1,28),
 (18,2,4),
 (19,2,5),
 (20,2,8),
 (21,2,9),
 (22,2,10),
 (23,2,11),
 (24,2,12),
 (25,1,13),
 (26,1,14),
 (27,1,15),
 (28,1,16),
 (29,1,17),
 (30,1,18),
 (31,1,19),
 (32,1,20),
 (33,1,21),
 (34,1,22),
 (35,1,23),
 (36,1,24),
 (37,1,27),
 (38,1,28),
 (39,3,4),
 (40,3,5),
 (41,3,11),
 (42,3,27),
 (43,3,28),
 (44,3,29),
 (45,3,30),
 (46,4,1),
 (47,4,2),
 (48,4,3),
 (49,4,4),
 (50,4,5),
 (51,4,6),
 (52,4,7),
 (53,4,8),
 (54,4,9),
 (55,4,10),
 (56,4,11),
 (57,4,12),
 (58,4,13),
 (59,4,14),
 (60,4,15),
 (61,4,16),
 (62,4,17),
 (63,4,18),
 (64,4,19),
 (65,4,20),
 (66,4,21),
 (67,4,22),
 (68,4,23),
 (69,4,24),
 (70,4,25),
 (71,4,26),
 (72,4,27),
 (73,4,28),
 (74,4,29),
 (75,4,30),
 (76,4,31),
 (77,4,32),
 (78,4,33);
/*!40000 ALTER TABLE `group_perm` ENABLE KEYS */;


--
-- Definition of table `groups`
--

DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `groups`
--

/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` (`id`,`name`) VALUES 
 (1,'Recording Officer'),
 (2,'BEAM'),
 (3,'BPAC'),
 (4,'Administrator');
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;


--
-- Definition of table `mpfr_submission`
--

DROP TABLE IF EXISTS `mpfr_submission`;
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
  KEY `mpfr_submission_7bdfbc04` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_d659cf48` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `mpfr_submission`
--

/*!40000 ALTER TABLE `mpfr_submission` DISABLE KEYS */;
/*!40000 ALTER TABLE `mpfr_submission` ENABLE KEYS */;


--
-- Definition of table `mpfro`
--

DROP TABLE IF EXISTS `mpfro`;
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
  KEY `mpfro_7bdfbc04` (`agency_id`),
  CONSTRAINT `activity_id_refs_id_69cee5cd` FOREIGN KEY (`activity_id`) REFERENCES `wfp_data` (`id`),
  CONSTRAINT `agency_id_refs_id_9d982146` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `mpfro`
--

/*!40000 ALTER TABLE `mpfro` DISABLE KEYS */;
/*!40000 ALTER TABLE `mpfro` ENABLE KEYS */;


--
-- Definition of table `mpfro_acc`
--

DROP TABLE IF EXISTS `mpfro_acc`;
CREATE TABLE `mpfro_acc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mpfro_id` int(11) NOT NULL,
  `p_target_id` int(11) NOT NULL,
  `target` int(11) NOT NULL,
  `accomplished` int(11) NOT NULL,
  `variance` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `p_target_id` (`p_target_id`),
  KEY `mpfro_acc_5a81952c` (`mpfro_id`),
  CONSTRAINT `mpfro_id_refs_id_641a2903` FOREIGN KEY (`mpfro_id`) REFERENCES `mpfro` (`id`),
  CONSTRAINT `p_target_id_refs_id_dddcf3da` FOREIGN KEY (`p_target_id`) REFERENCES `performancetarget` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `mpfro_acc`
--

/*!40000 ALTER TABLE `mpfro_acc` DISABLE KEYS */;
/*!40000 ALTER TABLE `mpfro_acc` ENABLE KEYS */;


--
-- Definition of table `notification`
--

DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `date_notify` date NOT NULL,
  `subject` varchar(45) NOT NULL,
  `msg` text NOT NULL,
  `agency_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_notification_1` (`agency_id`),
  CONSTRAINT `FK_notification_1` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `notification`
--

/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;


--
-- Definition of table `performancetarget`
--

DROP TABLE IF EXISTS `performancetarget`;
CREATE TABLE `performancetarget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wfp_activity_id` int(11) NOT NULL,
  `indicator` varchar(45) NOT NULL,
  `q1` int(11) NOT NULL,
  `q2` int(11) NOT NULL,
  `q3` int(11) NOT NULL,
  `q4` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `performancetarget_6297fd8e` (`wfp_activity_id`),
  CONSTRAINT `wfp_activity_id_refs_id_21d0b048` FOREIGN KEY (`wfp_activity_id`) REFERENCES `wfp_data` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `performancetarget`
--

/*!40000 ALTER TABLE `performancetarget` DISABLE KEYS */;
INSERT INTO `performancetarget` (`id`,`wfp_activity_id`,`indicator`,`q1`,`q2`,`q3`,`q4`) VALUES 
 (1,1,'No. Employees attending paraid',2,1,1,3),
 (2,1,'No. of Employees paid',2,1,1,3),
 (3,2,'No. machines repaired',2,2,2,2),
 (4,3,'No. machines repaired',2,2,2,2),
 (5,4,'No. machines repaired',2,2,2,2),
 (6,5,'No. machines repaired',2,2,2,2),
 (7,6,'No. machines repaired',2,2,2,2),
 (8,7,'No. of Employees paid',2,2,2,2),
 (9,7,'No. of Employees kick out',2,2,2,2);
/*!40000 ALTER TABLE `performancetarget` ENABLE KEYS */;


--
-- Definition of table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` varchar(10) NOT NULL,
  `target` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `permissions`
--

/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` (`id`,`action`,`target`) VALUES 
 (1,'add','agency'),
 (2,'edit','agency'),
 (3,'delete','agency'),
 (4,'view','agency information'),
 (5,'view','agency submitted documents'),
 (6,'add','agency submitted documents'),
 (7,'delete','agency submitted documents'),
 (8,'add','agency approved budget'),
 (9,'edit','agency approved budget'),
 (10,'delete','agency approved budget'),
 (11,'view','agency approved budget'),
 (12,'add','fund request'),
 (13,'edit','fund request'),
 (14,'delete','fund request'),
 (15,'view','running balances'),
 (16,'print','running balances'),
 (17,'view','status of allotment releases'),
 (18,'print','status of allotment releases'),
 (19,'view','total releases'),
 (20,'print','total releases'),
 (21,'view','monthly reports'),
 (22,'print','monthly reports'),
 (23,'view','quarterly report'),
 (24,'print','quarterly report'),
 (25,'view','transaction history'),
 (26,'delete','transaction history'),
 (27,'view','analysis report'),
 (28,'print','analysis report'),
 (29,'print','fund utilization'),
 (30,'view','fund utilization'),
 (31,'add','user'),
 (32,'edit','user'),
 (33,'view','user');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;


--
-- Definition of table `quarter_req_submit`
--

DROP TABLE IF EXISTS `quarter_req_submit`;
CREATE TABLE `quarter_req_submit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_id` int(11) NOT NULL,
  `requirement_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `quarter` int(11) NOT NULL,
  `date_submitted` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quarter_req_submit_7bdfbc04` (`agency_id`),
  KEY `quarter_req_submit_19c1813d` (`requirement_id`),
  CONSTRAINT `agency_id_refs_id_0c7100a2` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`),
  CONSTRAINT `requirement_id_refs_id_0589d44b` FOREIGN KEY (`requirement_id`) REFERENCES `quarterly_req` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `quarter_req_submit`
--

/*!40000 ALTER TABLE `quarter_req_submit` DISABLE KEYS */;
INSERT INTO `quarter_req_submit` (`id`,`agency_id`,`requirement_id`,`year`,`quarter`,`date_submitted`) VALUES 
 (1,1,1,2014,3,'2014-07-04');
/*!40000 ALTER TABLE `quarter_req_submit` ENABLE KEYS */;


--
-- Definition of table `quarterly_req`
--

DROP TABLE IF EXISTS `quarterly_req`;
CREATE TABLE `quarterly_req` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `quarterly_req`
--

/*!40000 ALTER TABLE `quarterly_req` DISABLE KEYS */;
INSERT INTO `quarterly_req` (`id`,`name`) VALUES 
 (1,'Statement of Allotment, Obligation and balances'),
 (2,'Status of Funds'),
 (3,'Reports of Detailed Disbursement'),
 (4,'Narrative Accomplishment Reports');
/*!40000 ALTER TABLE `quarterly_req` ENABLE KEYS */;


--
-- Definition of table `sector`
--

DROP TABLE IF EXISTS `sector`;
CREATE TABLE `sector` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sector`
--

/*!40000 ALTER TABLE `sector` DISABLE KEYS */;
INSERT INTO `sector` (`id`,`name`) VALUES 
 (1,'Environmental Conservation & Mgt & Human Settlement'),
 (2,'Regional Legislative Services'),
 (3,'Administrative & Financial management Services'),
 (4,'Health Services'),
 (5,'Education, Science & Technology'),
 (6,'Livelihood, Social Welfare and Protection Services'),
 (7,'Employment Promotion & Development & Industrial Peace'),
 (8,'Trade Industry & Investment Development'),
 (9,'Transportation & Communication Regulation Services'),
 (10,'Road Network, Public Infra & Other Development');
/*!40000 ALTER TABLE `sector` ENABLE KEYS */;


--
-- Definition of table `user_activity`
--

DROP TABLE IF EXISTS `user_activity`;
CREATE TABLE `user_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `action` varchar(100) NOT NULL,
  `act_date` datetime NOT NULL,
  `target` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_activity_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_1aa0dd1c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_activity`
--

/*!40000 ALTER TABLE `user_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_activity` ENABLE KEYS */;


--
-- Definition of table `user_group`
--

DROP TABLE IF EXISTS `user_group`;
CREATE TABLE `user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `user_group_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_e72894b0` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `user_id_refs_id_ce85507b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_group`
--

/*!40000 ALTER TABLE `user_group` DISABLE KEYS */;
INSERT INTO `user_group` (`id`,`user_id`,`group_id`) VALUES 
 (2,1,4);
/*!40000 ALTER TABLE `user_group` ENABLE KEYS */;


--
-- Definition of table `wfp_data`
--

DROP TABLE IF EXISTS `wfp_data`;
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
  KEY `wfp_data_7bdfbc04` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_89416cef` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `wfp_data`
--

/*!40000 ALTER TABLE `wfp_data` DISABLE KEYS */;
INSERT INTO `wfp_data` (`id`,`year`,`activity`,`agency_id`,`allocation`,`jan`,`feb`,`mar`,`apr`,`may`,`jun`,`jul`,`aug`,`sept`,`oct`,`nov`,`dec`,`total`) VALUES 
 (1,2014,'Salaries and Wages',1,'PS','23000.00','23000.00','2300.00','100.00','10000.00','0.00','0.00','0.00','0.00','1220.00','200.00','2000.00','61820.00'),
 (2,2014,'Maintenance',1,'MOOE','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','885456.00'),
 (3,2014,'Maintenance',1,'MOOE','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','885456.00'),
 (4,2014,'Maintenance',1,'MOOE','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','885456.00'),
 (5,2014,'Maintenance',1,'MOOE','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','885456.00'),
 (6,2014,'Maintenance',1,'MOOE','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','73788.00','885456.00'),
 (7,2014,'Extra Service',1,'CO','1000.00','1000.00','1000.00','1000.00','1000.00','1000.00','1000.00','1000.00','1000.00','1000.00','1000.00','1000.00','12000.00');
/*!40000 ALTER TABLE `wfp_data` ENABLE KEYS */;


--
-- Definition of table `wfp_submission`
--

DROP TABLE IF EXISTS `wfp_submission`;
CREATE TABLE `wfp_submission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_submitted` datetime NOT NULL,
  `year` int(11) NOT NULL,
  `agency_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wfp_submission_7bdfbc04` (`agency_id`),
  CONSTRAINT `agency_id_refs_id_83a1e54f` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `wfp_submission`
--

/*!40000 ALTER TABLE `wfp_submission` DISABLE KEYS */;
INSERT INTO `wfp_submission` (`id`,`date_submitted`,`year`,`agency_id`) VALUES 
 (1,'2014-07-05 00:33:22',2014,1);
/*!40000 ALTER TABLE `wfp_submission` ENABLE KEYS */;


--
-- Definition of view `user_permissions`
--

DROP TABLE IF EXISTS `user_permissions`;
DROP VIEW IF EXISTS `user_permissions`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `user_permissions` AS select `auth_user`.`id` AS `id`,`auth_user`.`username` AS `username`,`groups`.`name` AS `name`,`permissions`.`action` AS `action`,`permissions`.`target` AS `target` from ((((`auth_user` join `user_group` on((`user_group`.`user_id` = `auth_user`.`id`))) join `groups` on((`groups`.`id` = `user_group`.`group_id`))) join `group_perm` on((`group_perm`.`group_id` = `groups`.`id`))) join `permissions` on((`permissions`.`id` = `group_perm`.`permission_id`)));



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
