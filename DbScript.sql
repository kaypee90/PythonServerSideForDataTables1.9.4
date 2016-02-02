/*
SQLyog Ultimate v11.5 (64 bit)
MySQL - 10.1.9-MariaDB : Database - bucketlist
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`bucketlist` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `bucketlist`;

/*Table structure for table `tbl_role` */

DROP TABLE IF EXISTS `tbl_role`;

CREATE TABLE `tbl_role` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Rolename` varchar(50) DEFAULT NULL,
  UNIQUE KEY `Id` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_role` */

insert  into `tbl_role`(`Id`,`Rolename`) values (1,'Administrator'),(2,'Super User'),(3,'Client'),(4,'Support');

/*Table structure for table `tbl_user` */

DROP TABLE IF EXISTS `tbl_user`;

CREATE TABLE `tbl_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) DEFAULT NULL,
  `user_username` varchar(45) DEFAULT NULL,
  `user_password` varchar(45) DEFAULT NULL,
  `user_role` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_user` */

insert  into `tbl_user`(`user_id`,`user_name`,`user_username`,`user_password`,`user_role`) values (1,'Kofi','email','hasgin',1),(2,'James','Milner','hasgin',2),(3,'Kofi','Joep','yasins',1),(4,'Kwame','Adu','yasins',2),(5,'Yaw','Nkrumah','yasins',3),(6,'Ken','Addo','yassins',2),(7,'Geminma','Gloss','yassins',4),(8,'Judith','Amo','ysain',4),(9,'Josephine','Otoo','yasins',4);

/* Procedure structure for procedure `sp_createUser` */

/*!50003 DROP PROCEDURE IF EXISTS  `sp_createUser` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(20),
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(20)
)
BEGIN
    if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;
END */$$
DELIMITER ;

/* Procedure structure for procedure `sp_select_buckelist` */

/*!50003 DROP PROCEDURE IF EXISTS  `sp_select_buckelist` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_select_buckelist`(IN userid INT, OUT firstname varchar(50))
BEGIN
        IF userid = 0
        THEN
        SET firstname = 'Please enter a valid user id';
        ELSE
	SELECT user_name INTO firstname FROM tbl_user WHERE user_id = userid;
	END IF;
    END */$$
DELIMITER ;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
