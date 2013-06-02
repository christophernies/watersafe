# ************************************************************
# Sequel Pro SQL dump
# Version 3408
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.0.67)
# Database: watersafe
# Generation Time: 2013-06-02 16:38:23 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table PA_COUNTY_VIOLATION_RANK
# ------------------------------------------------------------

DROP TABLE IF EXISTS `PA_COUNTY_VIOLATION_RANK`;

CREATE TABLE `PA_COUNTY_VIOLATION_RANK` (
  `county_id` varchar(25) default NULL,
  `incident_count` int(11) default NULL,
  `rank` int(11) default NULL,
  `bucket` varchar(5) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

LOCK TABLES `PA_COUNTY_VIOLATION_RANK` WRITE;
/*!40000 ALTER TABLE `PA_COUNTY_VIOLATION_RANK` DISABLE KEYS */;

INSERT INTO `PA_COUNTY_VIOLATION_RANK` (`county_id`, `incident_count`, `rank`, `bucket`)
VALUES
	('42089',84,1,'R'),
	('42103',30,2,'R'),
	('42011',23,3,'R'),
	('42133',23,3,'R'),
	('42039',22,4,'R'),
	('42131',21,5,'R'),
	('42077',14,6,'Y'),
	('42043',14,6,'Y'),
	('42095',14,6,'Y'),
	('42111',12,7,'Y'),
	('42029',12,7,'Y'),
	('42015',11,8,'Y'),
	('42025',10,9,'Y'),
	('42107',9,10,'Y'),
	('42055',8,11,'Y'),
	('42075',8,11,'Y'),
	('42009',7,12,'Y'),
	('42115',7,12,'Y'),
	('42067',7,12,'Y'),
	('42123',6,13,'Y'),
	('42063',6,13,'Y'),
	('42065',6,13,'Y'),
	('42073',6,13,'Y'),
	('42041',5,14,'Y'),
	('42079',5,14,'Y'),
	('42003',4,15,'Y'),
	('42017',4,15,'Y'),
	('42051',4,15,'Y'),
	('42105',4,15,'Y'),
	('42045',3,16,'G'),
	('42049',3,16,'G'),
	('42113',2,17,'G'),
	('42081',2,17,'G'),
	('42013',2,17,'G'),
	('42047',2,17,'G'),
	('42061',2,17,'G'),
	('42109',2,17,'G'),
	('42083',1,18,'G'),
	('42085',1,18,'G'),
	('42129',1,18,'G'),
	('42087',1,18,'G'),
	('42019',1,18,'G'),
	('42021',1,18,'G'),
	('42059',1,18,'G'),
	('42091',1,18,'G'),
	('42023',1,18,'G'),
	('42093',1,18,'G'),
	('42027',1,18,'G'),
	('42097',1,18,'G'),
	('42101',1,18,'G'),
	('42031',1,18,'G'),
	('42069',1,18,'G'),
	('42033',1,18,'G'),
	('42071',1,18,'G'),
	('42035',1,18,'G');

/*!40000 ALTER TABLE `PA_COUNTY_VIOLATION_RANK` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
