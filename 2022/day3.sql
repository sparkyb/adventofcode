CREATE TABLE input (s TEXT);
.import day3.txt input

.mode line

WITH
  elves(elf, s) AS (
    SELECT
      row_number() OVER () - 1,
      s
    FROM input
  ),
  part1_items(elf, half, priority) AS (
    SELECT DISTINCT
      elf,
      (value - 1) * 2 / LENGTH(s),
      UNICODE(UPPER(SUBSTR(s, value, 1))) - UNICODE('A') + 1 + 26 * (UPPER(SUBSTR(s, value, 1)) = SUBSTR(s, value, 1))
    FROM elves, generate_series(1, LENGTH(s))
  ),
  part2_items(div, mod, priority) AS (
    SELECT DISTINCT
      elf / 3,
      elf % 3,
      priority
    FROM part1_items
  )
  SELECT
    (
      SELECT
        SUM(l.priority) AS part1
      FROM part1_items AS l, part1_items AS r
      WHERE
        l.half = 0 AND
        r.half = 1 AND
        l.elf = r.elf AND
        l.priority = r.priority
    ) AS part1,
    (
      SELECT
        SUM(a.priority) AS part2
      FROM part2_items AS a, part2_items AS b, part2_items AS c
      WHERE
        a.div = b.div AND
        a.div = c.div AND
        a.mod = 0 AND
        b.mod = 1 AND
        c.mod = 2 AND
        a.priority = b.priority AND
        a.priority = c.priority
    ) AS part2
  ;
