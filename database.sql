/**
 * sqlite3 opkg.db < database.sql
 */
DROP TABLE packages;
CREATE TABLE packages (id INTEGER, name VARCHAR, homepage VARCHAR, developer VARCHAR, dependency VARCHAR, source VARCHAR, description_short VARCHAR, packagelink VARCHAR, category VARCHAR, version VARCHAR);

DROP TABLE installed;
CREATE TABLE installed (id INTEGER, name VARCHAR, version VARCHAR);
