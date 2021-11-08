
-- mysql/mariadb

CREATE DATABASE IF NOT EXISTS asset CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS asset.inventory (
  sn VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255),
  description LONGTEXT,
  value DECIMAL(15,2),
  picture LONGBLOB,
  json JSON,
  note TEXT,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FULLTEXT(json),
  FULLTEXT(name, description, note),
  CHECK(JSON_VALID(json))
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


