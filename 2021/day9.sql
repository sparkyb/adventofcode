CREATE TABLE input (line TEXT);
.import day9.txt input

CREATE TABLE heights (y INTEGER, x INTEGER, height INTEGER);

INSERT INTO heights
SELECT
  input.rowid,
  value,
  SUBSTR(line, value, 1)
FROM input, generate_series(1, (SELECT MAX(LENGTH(line)) FROM input));

CREATE TABLE low_points(y INTEGER, x INTEGER, basin_size INTEGER);

INSERT INTO low_points
SELECT
  y,
  x,
  0
FROM heights AS h
WHERE
  NOT EXISTS (
    SELECT * FROM heights AS h2
    WHERE
      ((h2.x = h.x AND ABS(h2.y - h.y) = 1) OR (h2.y = h.y AND ABS(h2.x - h.x) = 1)) AND
      h2.height <= h.height
  );

WITH RECURSIVE
  basins(lp_y, lp_x, y, x) AS (
    SELECT
      y,
      x,
      y,
      x
    FROM low_points
    UNION
    SELECT
      lp_y,
      lp_x,
      h.y,
      h.x
    FROM basins AS b, heights AS h
    WHERE
      ((b.x = h.x AND ABS(b.y - h.y) = 1) OR (b.y = h.y AND ABS(b.x - h.x) = 1)) AND
      h.height < 9
  )
  UPDATE low_points AS lp
  SET
    basin_size=(SELECT COUNT(*) FROM basins WHERE lp.x=lp_x AND lp.y=lp_y);

.mode line

SELECT
  SUM(height + 1) AS part1
FROM low_points JOIN heights USING (y, x);

SELECT
  (SELECT basin_size FROM low_points ORDER BY basin_size DESC LIMIT 0, 1) *
  (SELECT basin_size FROM low_points ORDER BY basin_size DESC LIMIT 1, 1) *
  (SELECT basin_size FROM low_points ORDER BY basin_size DESC LIMIT 2, 1) AS part2;
