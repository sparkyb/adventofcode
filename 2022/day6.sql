CREATE TABLE input (s TEXT);

.import day6.txt input

.mode line

WITH RECURSIVE
  buffer(i, duplicates, current, rest) AS (
    SELECT
      0,
      0,
      '',
      s
    FROM input
    UNION ALL
    SELECT
      i + 1,
      duplicates
        - IIF(LENGTH(current) = 4 AND INSTR(SUBSTR(current, 2), SUBSTR(current, 1, 1)), 1, 0)
        + IIF(INSTR(SUBSTR(current, 2), SUBSTR(rest, 1, 1)), 1, 0),
      IIF(LENGTH(current) = 4, SUBSTR(current, 2), current) || SUBSTR(rest, 1, 1),
      SUBSTR(rest, 2)
    FROM buffer
    WHERE LENGTH(rest)
  )
  SELECT
    i AS part1
  FROM buffer
  WHERE
    i >= 4 AND duplicates = 0
  ORDER BY i
  LIMIT 1;

WITH RECURSIVE
  buffer(i, duplicates, current, rest) AS (
    SELECT
      0,
      0,
      '',
      s
    FROM input
    UNION ALL
    SELECT
      i + 1,
      duplicates
        - IIF(LENGTH(current) = 14 AND INSTR(SUBSTR(current, 2), SUBSTR(current, 1, 1)), 1, 0)
        + IIF(INSTR(SUBSTR(current, 2), SUBSTR(rest, 1, 1)), 1, 0),
      IIF(LENGTH(current) = 14, SUBSTR(current, 2), current) || SUBSTR(rest, 1, 1),
      SUBSTR(rest, 2)
    FROM buffer
    WHERE LENGTH(rest)
  )
  SELECT
    i AS part2
  FROM buffer
  WHERE
    i >= 14 AND duplicates = 0
  ORDER BY i
  LIMIT 1;
