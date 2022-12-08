CREATE TABLE grid(y INTEGER, x INTEGER, height);

WITH RECURSIVE
  lines(y, x, height, rest) AS (
    VALUES(
      0,
      -1,
      -1,
      CAST(readfile('day8.txt') AS TEXT)
    )
    UNION ALL
    SELECT
      IIF(SUBSTR(rest, 1, 1) = CHAR(10), y + 1, y),
      IIF(SUBSTR(rest, 1, 1) = CHAR(10), -1, x + 1),
      IIF(SUBSTR(rest, 1, 1) = CHAR(10), -1, CAST(SUBSTR(rest, 1, 1) AS INTEGER)),
      SUBSTR(rest, 2)
    FROM lines
    WHERE LENGTH(rest)
  )
  INSERT INTO grid
  SELECT y, x, height
  FROM lines
  WHERE height >= 0;

.mode lines

SELECT
  SUM(
    NOT EXISTS (
      SELECT
        height
      FROM grid AS cell2
      WHERE cell2.x < cell.x AND cell2.y = cell.y AND cell2.height >= cell.height
    ) OR
    NOT EXISTS (
      SELECT
        height
      FROM grid AS cell2
      WHERE cell2.y < cell.y AND cell2.x = cell.x AND cell2.height >= cell.height
    ) OR
    NOT EXISTS (
      SELECT
        height
      FROM grid AS cell2
      WHERE cell2.x > cell.x AND cell2.y = cell.y AND cell2.height >= cell.height
    ) OR
    NOT EXISTS (
      SELECT
        height
      FROM grid AS cell2
      WHERE cell2.y > cell.y AND cell2.x = cell.x AND cell2.height >= cell.height
    )
  ) AS part1,
  MAX(
    IFNULL((
      SELECT
        MIN(cell.x - cell2.x)
      FROM grid AS cell2
      WHERE cell2.x < cell.x AND cell2.y = cell.y AND cell2.height >= cell.height
    ), cell.x) *
    IFNULL((
      SELECT
        MIN(cell.y - cell2.y)
      FROM grid AS cell2
      WHERE cell2.y < cell.y AND cell2.x = cell.x AND cell2.height >= cell.height
    ), cell.y) *
    IFNULL((
      SELECT
        MIN(cell2.x - cell.x)
      FROM grid AS cell2
      WHERE cell2.x > cell.x AND cell2.y = cell.y AND cell2.height >= cell.height
    ), 98 - cell.x) *
    IFNULL((
      SELECT
        MIN(cell2.y - cell.y)
      FROM grid AS cell2
      WHERE cell2.y > cell.y AND cell2.x = cell.x AND cell2.height >= cell.height
    ), 98 - cell.y)
  ) AS part2
FROM grid AS cell;
