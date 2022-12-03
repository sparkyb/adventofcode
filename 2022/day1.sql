CREATE TABLE input (s TEXT);
INSERT INTO input VALUES(CAST (readfile('day1.txt') AS TEXT));

.mode line

WITH RECURSIVE
  elves(elf_num, elf, rest) AS (
    SELECT
      0,
      NULL,
      s  || CHAR(10) || CHAR(10)
    FROM input
    UNION ALL
    SELECT
      elf_num + 1,
      SUBSTR(rest, 1, INSTR(rest, CHAR(10) || CHAR(10)) - 1),
      SUBSTR(rest, INSTR(rest, CHAR(10) || CHAR(10)) + 2)
    FROM elves
    WHERE INSTR(rest, CHAR(10) || CHAR(10))
  ),
  calories(elf_num, item, rest) AS (
    SELECT
      elf_num,
      NULL,
      elf || CHAR(10)
    FROM elves
    WHERE elf IS NOT NULL
    UNION ALL
    SELECT
      elf_num,
      SUBSTR(rest, 1, INSTR(rest, CHAR(10)) - 1),
      SUBSTR(rest, INSTR(rest, CHAR(10)) + 1)
    FROM calories
    WHERE INSTR(rest, CHAR(10))
  ),
  calorie_sums(calorie_sum) AS (
    SELECT
      SUM(item)
    FROM calories
    WHERE item IS NOT NULL
    GROUP BY elf_num
  )
  SELECT
    FIRST_VALUE(calorie_sum) OVER win AS part1,
    SUM(calorie_sum) OVER win AS part2
  FROM calorie_sums
  WINDOW win AS (ORDER BY calorie_sum DESC ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING)
  ORDER BY calorie_sum DESC
  LIMIT 1;
