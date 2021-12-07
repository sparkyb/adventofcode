CREATE TABLE input (age INTEGER);
.separator ' ' ','
.import day6.txt input

.mode line

WITH RECURSIVE
  fish(day, n0, n1, n2, n3, n4, n5, n6, n7, n8) AS (
    SELECT
      0,
      SUM(age=0),
      SUM(age=1),
      SUM(age=2),
      SUM(age=3),
      SUM(age=4),
      SUM(age=5),
      SUM(age=6),
      SUM(age=7),
      SUM(age=8)
    FROM input
    UNION ALL
    SELECT
      day + 1,
      n1,
      n2,
      n3,
      n4,
      n5,
      n6,
      n7 + n0,
      n8,
      n0
    FROM fish
    WHERE day < 256
  )
  SELECT
    (SELECT n0+n1+n2+n3+n4+n5+n6+n7+n8 FROM fish WHERE day=80) AS part1,
    (SELECT n0+n1+n2+n3+n4+n5+n6+n7+n8 FROM fish WHERE day=256) AS part2;
