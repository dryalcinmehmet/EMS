CREATE TABLE test2 (
Date_Time TIMESTAMP NOT NULL,
Trafo_id VARCHAR(30) NOT NULL,
Active_Energy float
)


LOAD DATA LOCAL INFILE '/home/kereler/Desktop/temp/osos2.csv'
INTO TABLE test
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@Date_Time,Trafo_id,Active_Energy)
SET Date_Time = STR_TO_DATE(@Date_Time, '%Y-%m-%d %H:%i:%s')
;
