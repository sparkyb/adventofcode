CREATE TABLE input (x INTEGER);
.separator ' ' ','
.import day7.txt input

.mode line

WITH
  align(x, fuel) AS (
    SELECT
      value,
      (SELECT SUM(ABS(input.x - value)) FROM input)
    FROM generate_series((SELECT MIN(x) FROM input), (SELECT MAX(x) FROM input))
  )
  SELECT
    (SELECT MIN(fuel) FROM align) AS part1;

WITH
  align(x, fuel) AS (
    SELECT
      value,
      (SELECT SUM(ABS(input.x - value) * (ABS(input.x - value) + 1) / 2) FROM input)
    FROM generate_series((SELECT MIN(x) FROM input), (SELECT MAX(x) FROM input))
  )
  SELECT
    (SELECT MIN(fuel) FROM align) AS part2;
