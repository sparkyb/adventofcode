CREATE TABLE knots (knot INTEGER, y INTEGER, x INTEGER);
CREATE TABLE visited (
  knot INTEGER,
  y INTEGER,
  x INTEGER,
  UNIQUE (knot, y, x)
);

INSERT INTO knots
SELECT
  value,
  0,
  0
FROM generate_series(0, 9);

INSERT INTO visited
SELECT * FROM knots;

PRAGMA recursive_triggers=1;

CREATE TRIGGER drag AFTER UPDATE ON knots BEGIN
  INSERT OR IGNORE INTO visited VALUES (NEW.knot, NEW.y, NEW.x);
  UPDATE knots SET
    y = y + (MAX(ABS(NEW.y - y), ABS(NEW.x - x)) - 1) * SIGN(NEW.y - y),
    x = x + (MAX(ABS(NEW.y - y), ABS(NEW.x - x)) - 1) * SIGN(NEW.x - x)
  WHERE knot = NEW.knot + 1;
END;

CREATE TABLE moves (dy INTEGER, dx INTEGER);

CREATE TRIGGER move AFTER INSERT ON moves BEGIN
  UPDATE knots SET
    y = y + NEW.dy,
    x = x + NEW.dx
  WHERE knot = 0;
END;

WITH RECURSIVE
  head(dy, dx, n, rest) AS (
    VALUES (
      0,
      0,
      0,
      CAST(readfile('day9.txt') AS TEXT)
    )
    UNION ALL
    SELECT
      IIF(
        n = 0,
        CASE SUBSTR(rest, 1, 1)
          WHEN 'U' THEN -1
          WHEN 'D' THEN 1
          ELSE 0
        END,
        dy
      ),
      IIF(
        n = 0,
        CASE SUBSTR(rest, 1, 1)
          WHEN 'L' THEN -1
          WHEN 'R' THEN 1
          ELSE 0
        END,
        dx
      ),
      IIF(n = 0, CAST(SUBSTR(rest, 3, INSTR(rest, CHAR(10)) - 3) AS INTEGER), n - 1),
      IIF(n = 0, SUBSTR(rest, INSTR(rest, CHAR(10)) + 1), rest)
    FROM head
    WHERE n OR LENGTH(rest)
  )
  INSERT INTO moves
  SELECT
    dy,
    dx
  FROM head
  WHERE n;

.mode lines

SELECT
  COUNT(*) AS part1
FROM visited
WHERE knot = 1;

SELECT
  COUNT(*) AS part2
FROM visited
WHERE knot = 9;
