CREATE TABLE input (s TEXT);
CREATE TABLE numbers (i INTEGER, n TEXT);
CREATE TABLE final_boards (board_no INTEGER, board TEXT, step INTEGER, n INTEGER, num_sum INTEGER);

INSERT INTO input VALUES(CAST (readfile('day4.txt') AS TEXT));

WITH RECURSIVE
  number_parse(rest, i, n) AS (
    SELECT
      SUBSTR(s, 1, INSTR(s, CHAR(10)) - 1),
      0,
      NULL
    FROM input
    UNION ALL
    SELECT
      IIF(INSTR(rest, ','), SUBSTR(rest, INSTR(rest, ',') + 1), ''),
      i + 1,
      PRINTF('%02d', IIF(INSTR(rest, ','), SUBSTR(rest, 1, INSTR(rest, ',') - 1), rest))
    FROM number_parse
    WHERE LENGTH(rest) > 0
  )
  INSERT INTO numbers
  SELECT
    i,
    n
  FROM number_parse
  WHERE n IS NOT NULL;

.mode table

WITH RECURSIVE
  board_lines(rest, board_no, line) AS (
    SELECT
      SUBSTR(s, INSTR(s, CHAR(10)||CHAR(10)) + 2),
      0,
      ''
    FROM input
    UNION ALL
    SELECT
      SUBSTR(rest, INSTR(rest, CHAR(10)) + 1),
      IIF(line = '', board_no + 1, board_no),
      SUBSTR(rest, 1, INSTR(rest, CHAR(10)) - 1)
    FROM board_lines
    WHERE LENGTH(rest) > 0
  ),
  boards(step, board_no, n, board, num_sum) AS (
    SELECT
      0,
      board_no,
      NULL,
      GROUP_CONCAT(
        PRINTF('%02d', SUBSTR(line, 1, 2)) || ' ' ||
        PRINTF('%02d', SUBSTR(line, 4, 2)) || ' ' ||
        PRINTF('%02d', SUBSTR(line, 7, 2)) || ' ' ||
        PRINTF('%02d', SUBSTR(line, 10, 2)) || ' ' ||
        PRINTF('%02d', SUBSTR(line, 13, 2)) || CHAR(10),
        ''
      ),
      SUM(
        SUBSTR(line, 1, 2) +
        SUBSTR(line, 4, 2) +
        SUBSTR(line, 7, 2) +
        SUBSTR(line, 10, 2) +
        SUBSTR(line, 13, 2)
      )
    FROM board_lines
    WHERE board_no AND line != ''
    GROUP BY board_no
    UNION ALL
    SELECT
      step + 1,
      board_no,
      numbers.n,
      IIF(
        INSTR(board, numbers.n),
        SUBSTR(board, 1, INSTR(board, numbers.n) - 1) ||
          'XX' ||
          SUBSTR(board, INSTR(board, numbers.n) + 2),
        board
      ),
      IIF(INSTR(board, numbers.n), num_sum - numbers.n, num_sum)
    FROM boards, numbers
    WHERE
      step + 1 = i AND
      NOT regexp('XX XX XX XX XX', board) AND
      NOT regexp('(XX.{13}){4}XX', board)
  )
  INSERT INTO final_boards
  SELECT
    board_no,
    board,
    MAX(step),
    n,
    num_sum
  FROM boards
  GROUP BY board_no;

.mode line

SELECT
  n * num_sum AS part1
FROM final_boards
ORDER BY step ASC
LIMIT 1;

SELECT
  n * num_sum AS part2
FROM final_boards
ORDER BY step DESC
LIMIT 1;
