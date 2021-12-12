CREATE TABLE input (a TEXT, b TEXT);
.separator '-'
.import day12.txt input

CREATE TABLE edges (src TEXT, dest TEXT, small INTEGER);

INSERT INTO edges
SELECT
  a,
  b,
  LOWER(b) = b
FROM input
WHERE b != 'start' AND a != 'end';

INSERT INTO edges
SELECT
  b,
  a,
  LOWER(a) = a
FROM input
WHERE a != 'start' AND b != 'end';

.mode line

WITH RECURSIVE
  paths(path, tail, small2) AS (
    VALUES('start', 'start', 0)
    UNION ALL
    SELECT
      path || ',' || dest,
      dest,
      small2 OR (small AND INSTR(path, ',' || dest || ','))
    FROM paths LEFT JOIN edges ON (tail=src)
    WHERE
      NOT small OR
      NOT small2 OR
      NOT INSTR(path, ',' || dest || ',')
  )
  SELECT
    SUM(NOT small2) AS part1,
    COUNT(*) AS part2
  FROM paths
  WHERE tail = 'end';
