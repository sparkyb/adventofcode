CREATE TABLE input (n INTEGER);

.import day1.txt input

.mode line

WITH
  answer_lines(increased1, increased2) AS (
    SELECT
      n > (lag(n, 1) OVER (ROWS 1 PRECEDING)),
      n > (lag(n, 3) OVER (ROWS 3 PRECEDING))
    FROM input
  )
  SELECT
    SUM(increased1) AS part1,
    SUM(increased2) AS part2
  FROM answer_lines;
