CREATE TABLE input (n INTEGER);

WITH RECURSIVE
  input_lines(line, rest) AS (
    VALUES('', readfile('day1.txt')||CHAR(10))
    UNION ALL
    SELECT
      substr(rest, 1, instr(rest, CHAR(10)) - 1),
      substr(rest, instr(rest, CHAR(10)) + 1)
      FROM input_lines
      WHERE instr(rest, CHAR(10))
  )
  INSERT INTO input
  SELECT
    line AS n
  FROM input_lines
  WHERE line != '';

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
