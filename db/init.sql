CREATE DATABASE IF NOT EXISTS `os`;

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;

SET GLOBAL time_zone = 'America/New_York';
SET time_zone = 'America/New_York';


CREATE DATABASE IF NOT EXISTS bomblab;

CREATE TABLE IF NOT EXISTS bomblab.Submission (
       id INTEGER PRIMARY KEY AUTO_INCREMENT,
       ip VARCHAR(128),
       `date` VARCHAR(128),
       userid VARCHAR(128),
       userpwd VARCHAR(128),
       labid VARCHAR(128),
       `result` VARCHAR(2048)
);
