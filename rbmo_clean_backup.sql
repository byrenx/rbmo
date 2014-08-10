
/*Agency inserts*/
INSERT INTO `agency` VALUES (1,'TESDA',5,'tesda@gmail.com',''),(2,'Regional Budget and Management Office',6,'rbmo.armm@yahoo.com',''),(3,'Bureau on Cultural Heritage-ARMM',10,'bch.armm@yahoo.com',''),(4,'ARMM Development Academy',6,'ada.armm@yahho.com',''),(5,'Civil Aviation Authority of the Philippines',9,'DOTC@yahoo.com',''),(6,'Office for Southern Cultural Communities',6,'OSCC@yahoo.com',''),(7,'Housing and Land Use Regulatory Board',10,'HLURB@yahoo.com',''),(8,'Department of Science and Technology-ARMM',5,'DOST@yahoo.com',''),(9,'Cooperative Development Authority',6,'CDA@yahoo.com',''),(10,'Coordinating and Development Office on Bangsamoro Youth Affairs',6,'CDOBYA@yahoo.com',''),(11,'REZA-Polloc Freeport',10,'RPF@yahoo.com',''),(12,'Office of the Regional Governor',3,'ORG@yahoo.com',''),(13,'Administration of the Blue Mosque',3,'ABM@yahoo.com',''),(14,'Office of the Deputy Governors',3,'ODG@yahoo.com',''),(15,'Office of the Executive Secretary',3,'OESec@yahoo.com',''),(16,'Office of the Cabinet Secretary',3,'CabSec@yahoo.com',''),(17,'Office of the Chief Staff',3,'ChiefStaff@yahoo.com',''),(18,'Administrative Management Service',3,'AMS@yahoo.com',''),(19,'Finance and Budget Management Services',3,'FBMS@yahoo.com',''),(20,'Intelligence Security Services',3,'ISS@yahoo.com','');


/*user*/
INSERT INTO auth_user(id, username,first_name, last_name, email, password, is_superuser, is_staff, is_active, last_login, date_joined) VALUES 
(1,'byrenx@gmail.com','Jofel','Bayron','byrenx@gmail.com','pbkdf2_sha256$12000$RUq1qJjeOnTJ$Pg/flPPiPH/Vzb90FD1ewLqsHnrXXAJVJEZGRXhqKO0=',True,True,True,'2014-07-12 06:23:00','2014-07-12 01:47:07'),
(2,'rumzster@gmail.com','Rommel','Asibal','rumzster@gmail.com','pbkdf2_sha256$12000$dRrtHIaP4hLC$Pqi2r3TfURAIw62QqBvGQJPJ3/RFPYe/BZ8Ru8cKeik=',False,True,False,'2014-07-16 05:01:09','2014-07-12 06:23:43'),
(3,'sittie@gmail.com','Sittie','Bantayao','sittie@gmail.com','pbkdf2_sha256$12000$VmBFtEjIS5bf$7K3kFr8PRL6+50COmZdZBBHvLXJe2He7CPnciurXqW0=',False,True,False,'2014-07-17 00:33:05','2014-07-12 07:09:34'),
(4,'jessielibita.jcl@gmail.com','Jessie','Libita','jessielibita.jcl@gmail.com','pbkdf2_sha256$12000$wuQkIkDlRuvM$2bndJKBguLUgKrzypKVpDUJ7IC9UcrMjhNNVlpzR0Ms=',False,True,False,'2014-07-17 03:05:15','2014-07-12 07:11:43'),
(5,'helmiesalendab@gmail.com','helmie','salendab','helmiesalendab@gmail.com','pbkdf2_sha256$12000$k1RqU2onDRMg$JZKr2nLjF7LHW8fdp1NZ54Qa4xoPk20UYtzfgzyfmXA=',False,True,False,'2014-07-16 05:43:03','2014-07-16 03:15:23'),
(6,'test@gmail.com','test','Test','test@gmail.com','pbkdf2_sha256$12000$LjzcA2d3KUs1$WBUUuKXolxcw13ELVsCE3SSXF2FhglSnRrynwne5VXY=',False,True,False,'2014-07-16 03:32:36','2014-07-16 03:32:26'),
(8,'helmie_salendab@gmail.com','Helmie','Salendab','helmie_salendab@gmail.com','pbkdf2_sha256$12000$qg3NKad82gLA$mRK5cGlhZowTjh8uBi210FfldiKUio8oOT6AjcnUIKg=',False,True,False,'2014-07-16 05:41:16','2014-07-16 05:41:16');


/*co request insert*/
INSERT INTO co_request VALUES (1,'2014-12-12',2,'Request for release of Capital of RBMO','Transmitted to ORT for release','okay'),(2,'2014-07-14',2,'Request for release of PS for the month of July','Transmitted to ORT for release','Okay'),(3,'2014-07-16',3,'Request for realignment','Forwarded to ED','Pending for Approval');


/*contract of service submission insert*/
INSERT INTO `cos_submission` VALUES (1,2,'2014-07-14 01:47:26'),(2,2,'2014-07-15 08:59:45'),(3,3,'2014-07-16 03:49:49'),(4,5,'2014-07-16 06:34:56'),(5,4,'2014-07-16 08:46:12');


/* monthly reports submission */
INSERT INTO `mpfr_submission` VALUES (1,2014,2,'2014-07-14','2014-07-14','2014-07-14','2014-07-14','2014-07-14','2014-07-14','2014-07-15',NULL,NULL,NULL,NULL,NULL),(2,2014,5,'2014-07-16','2014-07-16','2014-07-16','2014-07-16','2014-07-16','2014-07-16',NULL,NULL,NULL,NULL,NULL,NULL);


/*quarter requirements submitted*/
INSERT INTO `quarter_req_submit` VALUES (1,2,1,2014,1,'2014-07-14'),(2,2,1,2014,2,'2014-07-14'),(3,2,2,2014,1,'2014-07-14'),(4,2,2,2014,2,'2014-07-14'),(5,2,3,2014,1,'2014-07-14'),(6,2,3,2014,2,'2014-07-14'),(7,2,4,2014,1,'2014-07-14'),(8,2,4,2014,2,'2014-07-14'),(9,2,1,2014,3,'2014-07-15'),(10,2,1,2014,4,'2014-07-15'),(11,3,1,2014,1,'2014-07-16'),(12,3,2,2014,1,'2014-07-16'),(13,3,3,2014,1,'2014-07-16'),(14,3,4,2014,1,'2014-07-16'),(15,5,1,2014,1,'2014-07-16'),(16,5,1,2014,2,'2014-07-16'),(17,5,2,2014,1,'2014-07-16'),(18,5,2,2014,2,'2014-07-16'),(19,5,3,2014,1,'2014-07-16'),(20,5,3,2014,2,'2014-07-16'),(21,5,4,2014,1,'2014-07-16'),(22,5,4,2014,2,'2014-07-16');

/*user group inserts*/
INSERT INTO `user_group` VALUES (1,1,4),(2,2,4),(3,3,4),(4,4,4),(5,5,2),(6,6,4),(7,8,4);
