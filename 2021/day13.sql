CREATE TABLE dots (fold INTEGER, x INTEGER, y INTEGER);

WITH RECURSIVE
  input(contents) AS (
    SELECT readfile('day13.txt')
  ),
  fold_lines(line, rest, axis, value) AS (
    SELECT
      0,
      SUBSTR(contents, INSTR(contents, CHAR(10)||CHAR(10)) + 2),
      NULL,
      NULL
    FROM input
    UNION ALL
    SELECT
      line + 1,
      SUBSTR(rest, INSTR(rest, CHAR(10)) + 1),
      CAST (SUBSTR(rest, INSTR(rest, '=') - 1, 1) AS TEXT),
      CAST (SUBSTR(rest, INSTR(rest, '=') + 1, INSTR(rest, CHAR(10)) - INSTR(rest, '=') - 1) AS INTEGER)
    FROM fold_lines
    WHERE LENGTH(rest) > 0
  ),
  folds(line, axis, value) AS (
    SELECT line, axis, value FROM fold_lines WHERE line > 0
  ),
  dot_lines(rest, x, y) AS (
    SELECT
      SUBSTR(contents, 1, INSTR(contents, CHAR(10)||CHAR(10))),
      NULL,
      NULL
    FROM input
    UNION ALL
    SELECT
      SUBSTR(rest, INSTR(rest, CHAR(10)) + 1),
      CAST (SUBSTR(rest, 1, INSTR(rest, ',') - 1) AS INTEGER),
      CAST (SUBSTR(rest, INSTR(rest, ',') + 1, INSTR(rest, CHAR(10)) - INSTR(rest, ',') - 1) AS INTEGER)
    FROM dot_lines
    WHERE LENGTH(rest) > 0
  ),
  dots_temp(fold, x, y) AS (
    SELECT 0, x, y FROM dot_lines WHERE x IS NOT NULL
    UNION
    SELECT
      fold + 1,
      IIF(axis = 'x' AND x > value, value - (x - value), x),
      IIF(axis = 'y' AND y > value, value - (y - value), y)
    FROM dots_temp, folds
    WHERE line = fold + 1
  )
  INSERT INTO dots SELECT * FROM dots_temp;

.mode line

SELECT COUNT(*) AS part1 FROM dots WHERE fold = 1;

WITH RECURSIVE
  final_dots(x, y) AS (
    SELECT x, y FROM dots WHERE fold=(SELECT MAX(fold) FROM dots)
  ),
  limits(max_x, max_y) AS (
    SELECT MAX(x), MAX(y) FROM final_dots
  ),
  image(line, x, y) AS (
    VALUES(CHAR(10), 0, 0)
    UNION ALL
    SELECT
      line ||
        IIF(EXISTS (
          SELECT
            1
          FROM final_dots
          WHERE image.x = final_dots.x AND image.y = final_dots.y
        ), '#', ' ') ||
        IIF(x = max_x, CHAR(10), ''),
      IIF(x = max_x, 0, x + 1),
      IIF(x = max_x, y + 1, y)
    FROM image, limits
    WHERE y <= max_y
  )
  SELECT
    line AS part2
  FROM image, limits
  WHERE y > max_y;

