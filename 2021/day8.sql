CREATE TABLE input (s0 TEXT, s1 TEXT, s2 TEXT, s3 TEXT, s4 TEXT, s5 TEXT, s6 TEXT, s7 TEXT, s8 TEXT, s9 TEXT, pipe TEXT, o1 TEXT, o2 TEXT, o3 TEXT, o4 TEXT);
.separator ' '
.import day8.txt input

CREATE TABLE signals (line INTEGER, wires TEXT);
CREATE TABLE outputs (line INTEGER, place INTEGER, wires TEXT);

INSERT INTO signals
SELECT
  rowid,
  s0
FROM input
UNION ALL
SELECT
  rowid,
  s1
FROM input
UNION ALL
SELECT
  rowid,
  s2
FROM input
UNION ALL
SELECT
  rowid,
  s3
FROM input
UNION ALL
SELECT
  rowid,
  s4
FROM input
UNION ALL
SELECT
  rowid,
  s5
FROM input
UNION ALL
SELECT
  rowid,
  s6
FROM input
UNION ALL
SELECT
  rowid,
  s7
FROM input
UNION ALL
SELECT
  rowid,
  s8
FROM input
UNION ALL
SELECT
  rowid,
  s9
FROM input;

INSERT INTO outputs
SELECT
  rowid,
  1000,
  o1
FROM input
UNION ALL
SELECT
  rowid,
  100,
  o2
FROM input
UNION ALL
SELECT
  rowid,
  10,
  o3
FROM input
UNION ALL
SELECT
  rowid,
  1,
  o4
FROM input;

UPDATE signals
SET
  wires=IIF(INSTR(wires, 'a'),'a','')||IIF(INSTR(wires, 'b'),'b','')||IIF(INSTR(wires, 'c'),'c','')||IIF(INSTR(wires, 'd'),'d','')||IIF(INSTR(wires, 'e'),'e','')||IIF(INSTR(wires, 'f'),'f','')||IIF(INSTR(wires, 'g'),'g','');

UPDATE outputs
SET
  wires=IIF(INSTR(wires, 'a'),'a','')||IIF(INSTR(wires, 'b'),'b','')||IIF(INSTR(wires, 'c'),'c','')||IIF(INSTR(wires, 'd'),'d','')||IIF(INSTR(wires, 'e'),'e','')||IIF(INSTR(wires, 'f'),'f','')||IIF(INSTR(wires, 'g'),'g','');

CREATE TABLE digits (line INTEGER, wires TEXT, digit INTEGER, UNIQUE (line, digit));

INSERT INTO digits
SELECT
  line,
  wires,
  1
FROM signals
WHERE LENGTH(wires)=2
UNION ALL
SELECT
  line,
  wires,
  7
FROM signals
WHERE LENGTH(wires)=3
UNION ALL
SELECT
  line,
  wires,
  4
FROM signals
WHERE LENGTH(wires)=4
UNION ALL
SELECT
  line,
  wires,
  8
FROM signals
WHERE LENGTH(wires)=7;

INSERT INTO digits
SELECT
  s.line,
  s.wires,
  6
FROM signals AS s, digits AS d1
WHERE
  s.line=d1.line AND
  d1.digit=1 AND
  LENGTH(s.wires)=6 AND
  (NOT INSTR(s.wires, SUBSTR(d1.wires, 1, 1)) OR NOT INSTR(s.wires, SUBSTR(d1.wires, 2, 1)));

INSERT INTO digits
SELECT
  s.line,
  s.wires,
  9
FROM signals AS s, digits AS d4
WHERE
  s.line=d4.line AND
  d4.digit=4 AND
  LENGTH(s.wires)=6 AND
  INSTR(s.wires, SUBSTR(d4.wires, 1, 1)) AND
  INSTR(s.wires, SUBSTR(d4.wires, 2, 1)) AND
  INSTR(s.wires, SUBSTR(d4.wires, 3, 1)) AND
  INSTR(s.wires, SUBSTR(d4.wires, 4, 1));

INSERT INTO digits
SELECT
  s.line,
  s.wires,
  0
FROM signals AS s LEFT JOIN digits AS d USING (line, wires)
WHERE
  LENGTH(s.wires)=6 AND
  d.digit IS NULL;

INSERT INTO digits
SELECT
  s.line,
  s.wires,
  3
FROM signals AS s, digits AS d1
WHERE
  s.line=d1.line AND
  d1.digit=1 AND
  LENGTH(s.wires)=5 AND
  INSTR(s.wires, SUBSTR(d1.wires, 1, 1)) AND
  INSTR(s.wires, SUBSTR(d1.wires, 2, 1));

INSERT INTO digits
SELECT
  s.line,
  s.wires,
  5
FROM signals AS s LEFT JOIN digits AS d USING (line, wires), digits AS d9
WHERE
  s.line=d9.line AND
  d9.digit=9 AND
  LENGTH(s.wires)=5 AND
  d.digit IS NULL AND
  INSTR(d9.wires, SUBSTR(s.wires, 1, 1)) AND
  INSTR(d9.wires, SUBSTR(s.wires, 2, 1)) AND
  INSTR(d9.wires, SUBSTR(s.wires, 3, 1)) AND
  INSTR(d9.wires, SUBSTR(s.wires, 4, 1)) AND
  INSTR(d9.wires, SUBSTR(s.wires, 5, 1));

INSERT INTO digits
SELECT
  s.line,
  s.wires,
  2
FROM signals AS s LEFT JOIN digits AS d USING (line, wires)
WHERE
  LENGTH(s.wires)=5 AND
  d.digit IS NULL;

.mode line

SELECT
  COUNT(*) AS part1
FROM outputs
WHERE LENGTH(wires) IN (2, 3, 4, 7);

SELECT
  SUM(digit * place) AS part2
FROM outputs JOIN digits USING (line, wires);
