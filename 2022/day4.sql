CREATE TABLE input (r0 TEXT, r1 TEXT);
.separator ','
.import day4.txt input

CREATE TABLE ranges (
  s0 INTEGER,
  e0 INTEGER,
  s1 INTEGER,
  e1 INTEGER,
  contains INTEGER AS ((s1 - s0) * (e1 - e0) <= 0),
  overlaps INTEGER AS ((e1 - s0) * (e0 - s1) >= 0)
);

INSERT INTO ranges
SELECT
  SUBSTR(r0, 1, INSTR(r0, '-') - 1),
  SUBSTR(r0, INSTR(r0, '-') + 1),
  SUBSTR(r1, 1, INSTR(r1, '-') - 1),
  SUBSTR(r1, INSTR(r1, '-') + 1)
FROM input;

.mode line

SELECT
  SUM(contains) AS part1,
  SUM(overlaps) AS part2
FROM ranges;
