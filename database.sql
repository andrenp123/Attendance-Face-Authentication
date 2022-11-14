DROP DATABASE IF EXISTS dbproject;
CREATE DATABASE dbproject;
USE dbproject;

CREATE TABLE tbljabatan(
idjabatan INT PRIMARY KEY,
jabatan VARCHAR(20),
gaji float
);

CREATE TABLE tblpegawai(
idpegawai VARCHAR(10) PRIMARY KEY,
namapegawai VARCHAR(255),
idjabatan INT,
FOREIGN KEY(idjabatan) REFERENCES tbljabatan(idjabatan)
);

CREATE TABLE login(
idpegawai VARCHAR(10),
password VARCHAR(255),
FOREIGN KEY(idpegawai) REFERENCES tblpegawai(idpegawai)
);

CREATE TABLE tblabsensi(
idpegawai VARCHAR(10),
checkin DATETIME,
checkout DATETIME,
FOREIGN KEY(idpegawai) REFERENCES tblpegawai(idpegawai)    
);

DROP EVENT IF EXISTS autopresensi;
CREATE EVENT autopresensi
ON SCHEDULE EVERY 1 MONTH
STARTS '2022-12-01 00:00:10'
ENDS '2035-12-31'
DO
    CALL spAutoAbsensi();

INSERT INTO tbljabatan VALUES
(0,'Administrator',20000000),
(1,'Direktur Utama',50000000),
(2,'Manager',15000000),
(3,'Supervisor',10000000),
(4,'Staff',5000000),
(5,'Controller',0);

INSERT INTO tblpegawai VALUES
('admin','Andre Nugroho Pranoto',0),
('dirut','Gracella Ignasha',1),
('mg01','David',2),
('spv01','Aviv',3),
('staff01','Agus',4),
('controller','Controller',5);



INSERT INTO login VALUES
('admin','123456'),
('dirut','123456'),
('mg01','123456'),
('spv01','123456'),
('staff01','123456'),
('controller','123456');


DELIMITER $$
CREATE PROCEDURE spAutoAbsensi()
BEGIN
DECLARE data INT DEFAULT 0;
DECLARE counter INT DEFAULT 0;
DECLARE i INT DEFAULT 0;
DECLARE startdate INT DEFAULT 1;
DECLARE enddate INT DEFAULT 0;
DECLARE pegawai VARCHAR(10);
DECLARE checker INT;
SELECT COUNT(*) FROM tblpegawai INTO data;
SELECT DAY(LAST_DAY(NOW())) INTO enddate;
WHILE counter<data DO
    SELECT idpegawai from tblpegawai limit counter,1 INTO pegawai;
    SET startdate=1;
    WHILE startdate<=enddate DO
        INSERT INTO tblabsensi VALUES(pegawai, CONCAT(LEFT(NOW(),8),startdate,' 23:57:58'), null);
        SET startdate=startdate+1;
    END WHILE;
    SET counter = counter+1;
END WHILE;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE spGetLogin()
BEGIN
    SELECT tblpegawai.idpegawai,login.password,tblpegawai.namapegawai
    FROM tblpegawai,login
    where tblpegawai.idpegawai=login.idpegawai;
END $$
DELIMITER ;
 

DELIMITER $$
CREATE PROCEDURE spGetNama(id VARCHAR(10))
BEGIN
    SELECT namapegawai 
    FROM tblpegawai 
    WHERE idpegawai=id;  

END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE spChecker(id VARCHAR(10),method VARCHAR(10),month VARCHAR(5))
BEGIN
    IF method='masuk' THEN
        SELECT COUNT(*) from tblabsensi WHERE idpegawai=id AND MONTH(checkin)=month AND
        (TIME(checkin)!='23:57:58' AND TIME(checkin)<'08:05:00');
    ELSE
        SELECT COUNT(*) from tblabsensi WHERE idpegawai=id AND MONTH(checkin)=month AND
        TIME(checkin)>'08:05:00';
    END IF;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE spInsertAbsensi(id VARCHAR(10),method VARCHAR(10))
BEGIN
DECLARE count INT;
    
    IF method='Checkin' THEN
        SELECT COUNT(*) FROM tblabsensi WHERE idpegawai=id AND DATE(checkin)=DATE(NOW()) AND
        checkin!=CONCAT(LEFT(NOW(),10),' 23:57:58') INTO count;
        IF count=0 THEN
            UPDATE tblabsensi
            SET checkin=NOW()
            WHERE idpegawai=id AND DATE(checkin)=DATE(NOW());
        END IF;
    ELSE
        SELECT COUNT(*) from tblabsensi WHERE idpegawai=id AND DATE(checkout)=DATE(NOW()) INTO count;
        IF count=0 THEN
           UPDATE tblabsensi
            SET checkout=NOW()
            WHERE idpegawai=id AND DATE(checkin)=DATE(NOW());
        END IF;
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE spInsertPegawai(id VARCHAR(10),nama VARCHAR(255),jabatan INT)
BEGIN
    INSERT INTO tblpegawai VALUES(id,nama,jabatan);
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER insert_login
AFTER INSERT ON tblpegawai FOR EACH ROW
BEGIN
    INSERT INTO login VALUES (NEW.idpegawai,'123456');
END $$
DELIMITER ;