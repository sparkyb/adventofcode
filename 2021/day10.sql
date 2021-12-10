CREATE TABLE input (line TEXT);
.import day10.txt input

.mode line

WITH RECURSIVE
  stack(rest,closers,corrupt) AS (
    SELECT line, '', 0 FROM input
    UNION ALL
    SELECT
      SUBSTR(rest, 2),
      CASE SUBSTR(rest, 1, 1)
        WHEN '(' THEN closers || ')'
        WHEN '[' THEN closers || ']'
        WHEN '{' THEN closers || '}'
        WHEN '<' THEN closers || '>'
        WHEN SUBSTR(closers, LENGTH(closers)) THEN SUBSTR(closers, 1, LENGTH(closers) - 1)
        ELSE NULL
      END,
      IIF(INSTR('([{<' || SUBSTR(closers, LENGTH(closers)), SUBSTR(rest, 1, 1)) = 0,
          CASE SUBSTR(rest, 1, 1)
            WHEN ')' THEN 3
            WHEN ']' THEN 57
            WHEN '}' THEN 1197
            WHEN '>' THEN 25137
          END,
          0)
    FROM stack
    WHERE corrupt = 0 AND LENGTH(rest) > 0
  ),
  incomplete(rest,score) AS (
    SELECT closers, 0 FROM stack WHERE corrupt = 0 AND LENGTH(rest) = 0
    UNION ALL
    SELECT
      SUBSTR(rest, 1, LENGTH(rest) - 1),
      5 * score + INSTR(')]}>', SUBSTR(rest, LENGTH(rest)))
    FROM incomplete
    WHERE LENGTH(rest) > 0
  )
  SELECT
    (SELECT SUM(corrupt) FROM stack) AS part1,
    (SELECT score FROM incomplete WHERE LENGTH(rest) = 0 ORDER BY score LIMIT (SELECT COUNT(*) / 2 FROM incomplete WHERE LENGTH(rest) = 0), 1) AS part2;
