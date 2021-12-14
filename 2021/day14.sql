CREATE TABLE input (s TEXT);
CREATE TABLE template (s TEXT);
CREATE TABLE rules (pair TEXT PRIMARY KEY, middle TEXT);
CREATE TABLE pairs (step INTEGER, pair TEXT, count INTEGER, UNIQUE (step, pair));
CREATE TABLE letters (step INTEGER, letter TEXT, count INTEGER, UNIQUE (step, letter));

INSERT INTO input VALUES(CAST (readfile('day14.txt') AS TEXT));
INSERT INTO template
SELECT
  SUBSTR(s, 1, INSTR(s, CHAR(10)) - 1)
FROM input;

WITH RECURSIVE
  rules_lines(rest, pair, middle) AS (
    SELECT
      SUBSTR(s, INSTR(s, CHAR(10)||CHAR(10)) + 2),
      NULL,
      NULL
    FROM input
    UNION ALL
    SELECT
      SUBSTR(rest, INSTR(rest, CHAR(10)) + 1),
      SUBSTR(rest, 1, 2) AS TEXT,
      SUBSTR(rest, 7, 1) AS TEXT
    FROM rules_lines
    WHERE LENGTH(rest) > 0
  )
  INSERT INTO rules
  SELECT pair, middle
  FROM rules_lines
  WHERE pair IS NOT NULL;

WITH RECURSIVE
  template_pairs(template, pairs_map) AS (
    SELECT
      s,
      '{}'
    FROM template
    UNION ALL
    SELECT
      SUBSTR(template, 2),
      json_set(
        pairs_map,
        '$.' || SUBSTR(template, 1, 2),
        COALESCE(
          json_extract(pairs_map, '$.' || SUBSTR(template, 1, 2)),
          0
        ) + 1
      )
    FROM template_pairs
    WHERE LENGTH(template) > 1
  ),
  json_pairs(step, pairs_map) AS (
    SELECT
      0,
      pairs_map
    FROM template_pairs
    WHERE LENGTH(template) = 1
    UNION ALL
    SELECT
      step + 1,
      (
        SELECT
          json_group_object(
            pair,
            (
              SELECT
                COALESCE(SUM(value), 0)
              FROM json_each(pairs_map) LEFT JOIN rules AS r ON (key = pair)
              WHERE
                SUBSTR(key, 1, 1) || r.middle = new_pair.pair OR
                r.middle || SUBSTR(key, 2, 1) = new_pair.pair
            )
          )
        FROM rules AS new_pair
      )
    FROM json_pairs
    WHERE step < 40
  )
  INSERT INTO pairs
  SELECT
    step,
    key,
    value
  FROM json_pairs, json_each(pairs_map);

INSERT INTO letters
SELECT
  step,
  SUBSTR(pair, 1, 1),
  count
FROM pairs
UNION ALL
SELECT
  step,
  SUBSTR(pair, 2, 1),
  count
FROM pairs
WHERE 1
ON CONFLICT DO UPDATE SET
  count = count + excluded.count;

UPDATE letters SET
count = count + 1
WHERE
  letter = (SELECT SUBSTR(s, 1, 1) FROM template) OR
  letter = (SELECT SUBSTR(s, LENGTH(s), 1) FROM template);

UPDATE letters SET
count = count / 2;

.mode line

SELECT MAX(count) - MIN(count) AS part1 FROM letters WHERE step=10;
SELECT MAX(count) - MIN(count) AS part2 FROM letters WHERE step=40;
