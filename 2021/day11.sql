CREATE TABLE input_lines (line TEXT);
.import day11.txt input_lines

.mode line

WITH RECURSIVE
  steps(step, iter, grid, flashes) AS (
    SELECT
      0,
      0,
      '000000000000' || CHAR(10) ||
      '0' || GROUP_CONCAT(line, '0' || CHAR(10) || '0') || '0' || CHAR(10) ||
      '000000000000' || CHAR(10),
      0
    FROM input_lines
    UNION ALL
    SELECT
      IIF(INSTR(grid, 'A'), step, step + 1),
      IIF(INSTR(grid, 'A'), iter + 1, 0),
      '000000000000' || CHAR(10) ||
      '0' || IIF(INSTR(grid, 'A'),
        (
          SELECT
            GROUP_CONCAT(
              CASE SUBSTR(grid, 15 + (value / 10) * 13 + value % 10, 1)
                WHEN 'A' THEN '0'
                WHEN '0' THEN '0'
                ELSE
                  PRINTF(
                    '%X',
                    MIN(
                      SUBSTR(grid, 15 + (value / 10) * 13 + value % 10, 1) +
                      (SUBSTR(grid, 15 + ((value / 10) - 1) * 13 + value % 10 - 1, 1)='A') +
                      (SUBSTR(grid, 15 + ((value / 10) - 1) * 13 + value % 10, 1)='A') +
                      (SUBSTR(grid, 15 + ((value / 10) - 1) * 13 + value % 10 + 1, 1)='A') +
                      (SUBSTR(grid, 15 + (value / 10) * 13 + value % 10 - 1, 1)='A') +
                      (SUBSTR(grid, 15 + (value / 10) * 13 + value % 10 + 1, 1)='A') +
                      (SUBSTR(grid, 15 + ((value / 10) + 1) * 13 + value % 10 - 1, 1)='A') +
                      (SUBSTR(grid, 15 + ((value / 10) + 1) * 13 + value % 10, 1)='A') +
                      (SUBSTR(grid, 15 + ((value / 10) + 1) * 13 + value % 10 + 1, 1)='A'),
                      10))
              END ||
              IIF(value % 10 = 9, '0' || CHAR(10) || '0', ''), '')
          FROM generate_series(0, 99)
        ),
        (
          SELECT
            GROUP_CONCAT(
              PRINTF('%X', SUBSTR(grid, 15 + (value / 10) * 13 + value % 10, 1) + 1) ||
              IIF(value % 10 = 9, '0' || CHAR(10) || '0', ''), '')
          FROM generate_series(0, 99)
        )
      ) || '00000000000' || CHAR(10),
      IIF(INSTR(grid, 'A'), flashes + (SELECT SUM(SUBSTR(grid, value, 1)='A') FROM generate_series(1, LENGTH(grid))), 0)
    FROM steps
    WHERE flashes < 100
  )
  SELECT
    (
      SELECT
        SUM(flashes)
      FROM steps AS s
      WHERE step <= 100 AND iter=(SELECT MAX(iter) FROM steps AS s2 WHERE s.step = s2. step)
    ) AS part1,
    (SELECT step FROM steps WHERE flashes = 100 LIMIT 1) AS part2;
