CREATE TABLE input (line TEXT);
.import day3.txt input

.mode line

WITH
  digits(pos, count) AS (
    SELECT
      value - 1,
      SUM(ifnull(nullif(substr(line, -value, 1), '') * 2 - 1, 0))
    FROM input, generate_series(1, 12)
    GROUP BY value
  ),
  rates(gamma, epsilon) AS (
    SELECT
      SUM(CAST(pow(2, pos) AS INTEGER) * (count > 0)) AS gamma,
      SUM(CAST(pow(2, pos) AS INTEGER) * (count < 0)) AS epsilon
    FROM digits
  )
  SELECT
    gamma,
    epsilon,
    gamma * epsilon AS part1
  FROM rates;

WITH RECURSIVE
  prefix_digits(prefix, count) AS (
    SELECT
      substr(line, 1, value - 1),
      SUM(ifnull(nullif(substr(line, value, 1), '') * 2 - 1, 0))
    FROM input, generate_series(1, 12)
    GROUP BY substr(line, 1, value - 1)
  ),
  filtered_nums(name, prefix_len, line) AS (
    SELECT
      name,
      0,
      line
    FROM input, (SELECT 'o2' AS name UNION SELECT 'co2' AS name)
    UNION ALL
    SELECT
      name,
      prefix_len + 1,
      line
    FROM filtered_nums
    WHERE substr(line, prefix_len + 1, 1) = (SELECT ''||(CASE name WHEN 'o2' THEN count >= 0 ELSE count < 0 END) FROM prefix_digits WHERE prefix = substr(line, 1, prefix_len))
  ),
  ratings(name, prefix_len, value) AS (
    SELECT
      name,
      max(prefix_len),
      (SELECT SUM(CAST(POW(2, LENGTH(line) - value) AS INTEGER) * substr(line, value, 1)) FROM generate_series(1, LENGTH(line)))
    FROM filtered_nums
    GROUP BY name
  ),
  answer_parts(o2, co2) AS (
    SELECT
      (SELECT value FROM ratings WHERE name='o2') AS o2,
      (SELECT value FROM ratings WHERE name='co2') AS co2
  )
  SELECT
    o2,
    co2,
    o2 * co2 AS part2
  FROM answer_parts;
