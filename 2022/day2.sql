CREATE TABLE input (opponent TEXT, move_result TEXT);
.separator ' '
.import day2.txt input

CREATE TABLE games (
  opponent INTEGER,
  move_result INTEGER,
  result_part1 INTEGER AS ((move_result - opponent + 4) % 3),
  move_part2 INTEGER AS ((opponent + move_result + 2) % 3),
  score_part1 INTEGER AS (move_result + 1 + result_part1 * 3),
  score_part2 INTEGER AS (move_part2 + 1 + move_result * 3)
);

INSERT INTO games (opponent, move_result)
SELECT
  INSTR('ABC', opponent) - 1,
  INSTR('XYZ', move_result) - 1
FROM input;

.mode line

SELECT
  SUM(score_part1) AS part1,
  SUM(score_part2) AS part2
FROM games;
