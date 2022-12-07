CREATE TABLE directories (path TEXT, size INTEGER);

WITH RECURSIVE
  lines(line, cwd, path, size, rest) AS (
    VALUES (
      '',
      '',
      '',
      0,
      CAST (readfile('day7.txt') AS TEXT)
    )
    UNION ALL
    SELECT
      SUBSTR(rest, 1, INSTR(rest, CHAR(10)) - 1),
      CASE
        WHEN SUBSTR(rest, 1, 6) = '$ cd /' THEN
          ''
        WHEN SUBSTR(rest, 1, 7) = '$ cd ..' THEN
          SUBSTR(cwd, INSTR(cwd, '/') + 1)
        WHEN SUBSTR(rest, 1, 5) = '$ cd ' THEN
          SUBSTR(rest, 6, INSTR(rest, CHAR(10)) - 6) || '/' || cwd
        ELSE
          cwd
      END,
      CASE
        WHEN SUBSTR(rest, 1, 1) != '$' AND SUBSTR(rest, 1, 4) != 'dir ' AND LENGTH(path) THEN
          SUBSTR(path, INSTR(path, '/') + 1)
        ELSE
          cwd
      END,
      CASE
        WHEN SUBSTR(rest, 1, 1) != '$' AND SUBSTR(rest, 1, 4) != 'dir ' THEN
          CAST(SUBSTR(rest, 1, INSTR(rest, ' ') - 1) AS INTEGER)
        ELSE
          0
      END,
      CASE
        WHEN SUBSTR(rest, 1, 1) = '$' OR SUBSTR(rest, 1, 4) = 'dir ' OR LENGTH(path) = 0 THEN
          SUBSTR(rest, INSTR(rest, CHAR(10)) + 1)
        ELSE
          rest
      END
    FROM lines
    WHERE LENGTH(rest)
  )
  INSERT INTO directories
  SELECT
    path,
    SUM(size)
  FROM lines
  WHERE size > 0
  GROUP BY path;

.mode lines

SELECT
  SUM(size) AS part1
FROM directories
WHERE size <= 100000;


SELECT
  MIN(size) AS part2
FROM directories
WHERE size >= 30000000 - (70000000 - (SELECT size FROM directories WHERE path = ''));
