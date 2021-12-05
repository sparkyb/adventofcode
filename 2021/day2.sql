CREATE TABLE input (dir TEXT, amount INTEGER);
.separator ' '
.import day2.txt input

.mode line

WITH
  answer_lines(dx, dy, aim) AS (
    SELECT
      CASE dir WHEN 'forward' THEN amount ELSE 0 END,
      CASE dir WHEN 'down' THEN amount WHEN 'up' THEN -amount ELSE 0 END,
      SUM(CASE dir WHEN 'down' THEN amount WHEN 'up' THEN -amount ELSE 0 END)
        OVER (ROWS UNBOUNDED PRECEDING)
    FROM input
  ),
  answer(position, depth1, depth2) AS (
    SELECT SUM(dx), SUM(dy), SUM(dx * aim)
    FROM answer_lines
  )
  SELECT
    position * depth1 AS part1,
    position * depth2 AS part2
  FROM answer;
