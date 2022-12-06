CREATE TABLE input (contents TEXT);
INSERT INTO input VALUES(CAST (readfile('day5.txt') AS TEXT));

CREATE TABLE steps (
  step INTEGER,
  n INTEGER,
  f INTEGER,
  t INTEGER
);

WITH RECURSIVE
  step_lines(i, n, f, t, rest) AS (
    SELECT
      0,
      0,
      0,
      0,
      SUBSTR(contents, INSTR(contents, CHAR(10, 10)) + 2)
    FROM input
    UNION ALL
    SELECT
      i + 1,
      SUBSTR(rest, 6, INSTR(rest, ' from ') - 6),
      SUBSTR(rest, INSTR(rest, ' from ') + 6, INSTR(rest, ' to ') - INSTR(rest, ' from ') - 6),
      SUBSTR(rest, INSTR(rest, ' to ') + 4, INSTR(rest, CHAR(10)) - INSTR(rest, ' to ') - 4),
      SUBSTR(rest, INSTR(rest, CHAR(10)) + 1)
    FROM step_lines
    WHERE LENGTH(rest)
  )
  INSERT INTO steps
  SELECT i, n, f, t FROM step_lines WHERE i > 0;

CREATE TABLE starting_stacks (
  s1 TEXT,
  s2 TEXT,
  s3 TEXT,
  s4 TEXT,
  s5 TEXT,
  s6 TEXT,
  s7 TEXT,
  s8 TEXT,
  s9 TEXT
);

WITH RECURSIVE
  stack_lines(s1, s2, s3, s4, s5, s6, s7, s8, s9, rest) AS (
    SELECT
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      SUBSTR(contents, 1, INSTR(contents, CHAR(10, 10)) - 36)
    FROM input
    UNION ALL
    SELECT
      SUBSTR(rest, 2 + 4 * 0, 1),
      SUBSTR(rest, 2 + 4 * 1, 1),
      SUBSTR(rest, 2 + 4 * 2, 1),
      SUBSTR(rest, 2 + 4 * 3, 1),
      SUBSTR(rest, 2 + 4 * 4, 1),
      SUBSTR(rest, 2 + 4 * 5, 1),
      SUBSTR(rest, 2 + 4 * 6, 1),
      SUBSTR(rest, 2 + 4 * 7, 1),
      SUBSTR(rest, 2 + 4 * 8, 1),
      SUBSTR(rest, INSTR(rest, CHAR(10)) + 1)
    FROM stack_lines
    WHERE LENGTH(rest)
  )
  INSERT INTO starting_stacks
  SELECT
    LTRIM(GROUP_CONCAT(s1, '')) AS s1,
    LTRIM(GROUP_CONCAT(s2, '')) AS s2,
    LTRIM(GROUP_CONCAT(s3, '')) AS s3,
    LTRIM(GROUP_CONCAT(s4, '')) AS s4,
    LTRIM(GROUP_CONCAT(s5, '')) AS s5,
    LTRIM(GROUP_CONCAT(s6, '')) AS s6,
    LTRIM(GROUP_CONCAT(s7, '')) AS s7,
    LTRIM(GROUP_CONCAT(s8, '')) AS s8,
    LTRIM(GROUP_CONCAT(s9, '')) AS s9
  FROM stack_lines;

.mode lines

WITH RECURSIVE
  moves(step, s1, s2, s3, s4, s5, s6, s7, s8, s9, temp) AS (
    SELECT
      1, s1, s2, s3, s4, s5, s6, s7, s8, s9, ''
    FROM starting_stacks
    UNION ALL
    SELECT
      CASE n - LENGTH(temp)
        WHEN 0 THEN step + 1
        ELSE step
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 1, temp, '') || s1
        ELSE IIF(f = 1, SUBSTR(s1, 2), s1)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 2, temp, '') || s2
        ELSE IIF(f = 2, SUBSTR(s2, 2), s2)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 3, temp, '') || s3
        ELSE IIF(f = 3, SUBSTR(s3, 2), s3)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 4, temp, '') || s4
        ELSE IIF(f = 4, SUBSTR(s4, 2), s4)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 5, temp, '') || s5
        ELSE IIF(f = 5, SUBSTR(s5, 2), s5)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 6, temp, '') || s6
        ELSE IIF(f = 6, SUBSTR(s6, 2), s6)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 7, temp, '') || s7
        ELSE IIF(f = 7, SUBSTR(s7, 2), s7)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 8, temp, '') || s8
        ELSE IIF(f = 8, SUBSTR(s8, 2), s8)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 9, temp, '') || s9
        ELSE IIF(f = 9, SUBSTR(s9, 2), s9)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN ''
        ELSE SUBSTR(
          CASE f
            WHEN 1 THEN s1
            WHEN 2 THEN s2
            WHEN 3 THEN s3
            WHEN 4 THEN s4
            WHEN 5 THEN s5
            WHEN 6 THEN s6
            WHEN 7 THEN s7
            WHEN 8 THEN s8
            WHEN 9 THEN s9
          END,
          1,
          1) || temp
      END
    FROM moves
    JOIN steps USING (step)
  )
  SELECT
    SUBSTR(s1, 1, 1) ||
    SUBSTR(s2, 1, 1) ||
    SUBSTR(s3, 1, 1) ||
    SUBSTR(s4, 1, 1) ||
    SUBSTR(s5, 1, 1) ||
    SUBSTR(s6, 1, 1) ||
    SUBSTR(s7, 1, 1) ||
    SUBSTR(s8, 1, 1) ||
    SUBSTR(s9, 1, 1) AS part1
  FROM moves
  ORDER BY step DESC
  LIMIT 1;

WITH RECURSIVE
  moves(step, s1, s2, s3, s4, s5, s6, s7, s8, s9, temp) AS (
    SELECT
      1, s1, s2, s3, s4, s5, s6, s7, s8, s9, ''
    FROM starting_stacks
    UNION ALL
    SELECT
      CASE n - LENGTH(temp)
        WHEN 0 THEN step + 1
        ELSE step
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 1, temp, '') || s1
        ELSE IIF(f = 1, SUBSTR(s1, n + 1), s1)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 2, temp, '') || s2
        ELSE IIF(f = 2, SUBSTR(s2, n + 1), s2)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 3, temp, '') || s3
        ELSE IIF(f = 3, SUBSTR(s3, n + 1), s3)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 4, temp, '') || s4
        ELSE IIF(f = 4, SUBSTR(s4, n + 1), s4)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 5, temp, '') || s5
        ELSE IIF(f = 5, SUBSTR(s5, n + 1), s5)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 6, temp, '') || s6
        ELSE IIF(f = 6, SUBSTR(s6, n + 1), s6)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 7, temp, '') || s7
        ELSE IIF(f = 7, SUBSTR(s7, n + 1), s7)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 8, temp, '') || s8
        ELSE IIF(f = 8, SUBSTR(s8, n + 1), s8)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN IIF(t = 9, temp, '') || s9
        ELSE IIF(f = 9, SUBSTR(s9, n + 1), s9)
      END,
      CASE n - LENGTH(temp)
        WHEN 0 THEN ''
        ELSE SUBSTR(
          CASE f
            WHEN 1 THEN s1
            WHEN 2 THEN s2
            WHEN 3 THEN s3
            WHEN 4 THEN s4
            WHEN 5 THEN s5
            WHEN 6 THEN s6
            WHEN 7 THEN s7
            WHEN 8 THEN s8
            WHEN 9 THEN s9
          END,
          1,
          n)
      END
    FROM moves
    JOIN steps USING (step)
  )
  SELECT
    SUBSTR(s1, 1, 1) ||
    SUBSTR(s2, 1, 1) ||
    SUBSTR(s3, 1, 1) ||
    SUBSTR(s4, 1, 1) ||
    SUBSTR(s5, 1, 1) ||
    SUBSTR(s6, 1, 1) ||
    SUBSTR(s7, 1, 1) ||
    SUBSTR(s8, 1, 1) ||
    SUBSTR(s9, 1, 1) AS part2
  FROM moves
  ORDER BY step DESC
  LIMIT 1;
