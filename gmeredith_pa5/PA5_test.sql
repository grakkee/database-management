-- CS457 PA5
-- 
-- This is an bonus assignment. It is NOT required.
-- It will be counted as five (5) points; thus, the overall possible points you can get are 105.
--
-- Grading: 1 point for design document, 1 point for coding style, and 3 points for three aggregate queries (i.e., COUNT, AVG, and MAX).

CREATE DATABASE db_tpch;
USE db_tpch;

CREATE TABLE Part (Partkey int, Size int);

INSERT INTO Part VALUES(1, 7);
INSERT INTO Part VALUES(2, 1);
INSERT INTO Part VALUES(3, 21);
INSERT INTO Part VALUES(4, 14);
INSERT INTO Part VALUES(5, 15);
INSERT INTO Part VALUES(6, 4);
INSERT INTO Part VALUES(7, 45);
INSERT INTO Part VALUES(8, 41);
INSERT INTO Part VALUES(9, 12);
INSERT INTO Part VALUES(10, 44);

SELECT COUNT(*) FROM Part;

SELECT AVG(Size) FROM Part;

SELECT MAX(Size) FROM Part;

.EXIT

-- Expected output
--
-- Database db_tpch created.
-- Using database db_tpch.
--
-- Table Part created.
--
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
--
-- COUNT(*)
-- 10
--
-- AVG(Size)
-- 20.4
--
-- MAX(Size)
-- 45
--
-- All done.