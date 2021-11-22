CREATE DATABASE MYSQLTEST;
use MYSQLTEST;

CREATE TABLE impressions (
  impressionTime DATETIME,
  impressionId INT,
  adId INT,
  visitorHash VARCHAR(100)
);
CREATE TABLE clicks (
    clickTimestamp DATETIME,
    impressionId INT
);