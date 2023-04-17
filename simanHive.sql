CREATE DATABASE IF NOT EXISTS simandata;

USE simandata;

CREATE EXTERNAL TABLE IF NOT EXISTS simanproductsdata(Name STRING, Brand STRING, Image STRING, Discount INT, Link STRING, Price INT, PriceWithDiscount INT)

COMMENT 'Products of siman store'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hdfs/simanData/cleanData';
