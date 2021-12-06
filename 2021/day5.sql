CREATE TABLE input_lines (line TEXT);
.import day5.txt input_lines

CREATE TABLE input (x1 INTEGER, y1 INTEGER, x2 INTEGER, y2 INTEGER);

INSERT INTO input
SELECT
  SUBSTR(line, 1, INSTR(line, ',') - 1),
  SUBSTR(line, INSTR(line, ',') + 1, INSTR(line, ' -> ') - INSTR(line, ',')),
  SUBSTR(line, INSTR(line, ' -> ') + 4, INSTR(SUBSTR(line, INSTR(line, ' -> ') + 4), ',') - 1),
  SUBSTR(line, INSTR(line, ' -> ') + 4 + INSTR(SUBSTR(line, INSTR(line, ' -> ') + 4), ','))
FROM input_lines;

.mode line

WITH
  points(x, y, part1) AS (
    SELECT
      x1 + value * SIGN(x2 - x1),
      y1 + value * SIGN(y2 - y1),
      x1 = x2 OR y1 = y2
    FROM input, generate_series(0, MAX(ABS(x2 - x1), ABS(y2 - y1)))
  ),
  point_counts(x, y, count1, count2) AS (
    SELECT
      x,
      y,
      SUM(part1),
      COUNT(*)
    FROM points
    GROUP BY x, y
  )
  SELECT
    SUM(count1 > 1) AS part1,
    SUM(count2 > 1) AS part2
  FROM point_counts;
