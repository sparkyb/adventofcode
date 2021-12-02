CREATE TABLE input (dir TEXT, amount INTEGER);

WITH RECURSIVE
  input_lines(line, rest) AS (
    VALUES('', readfile('day2.txt')||CHAR(10))
    UNION ALL
    SELECT
      substr(rest, 1, instr(rest, CHAR(10)) - 1),
      substr(rest, instr(rest, CHAR(10)) + 1)
      FROM input_lines
      WHERE instr(rest, CHAR(10))
  )
  INSERT INTO input
  SELECT
    substr(line, 1, instr(line, ' ') - 1) AS dir,
    substr(line, instr(line, ' ') + 1) AS amount
  FROM input_lines
  WHERE line != '';

.mode line

WITH
  answer_lines(dx, dy, aim) AS (
    SELECT
      CASE WHEN dir = 'forward' THEN amount ELSE 0 END,
      CASE WHEN dir = 'down' THEN amount WHEN dir = 'up' THEN -amount ELSE 0 END,
      SUM(CASE WHEN dir = 'down' THEN amount WHEN dir = 'up' THEN -amount ELSE 0 END)
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
