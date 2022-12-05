Advent Of Code
==============

These are all my solutions to [Advent of Code](https://adventofcode.com/). I
solve in Python for speed (although I clean up the code a bit afterwards) and
starting in 2021 I decided to see how far I could get with SQLite and
[Google Sheets][sheets] for fun. The former two are in this repo, the [Google
Sheets solutions][sheets] are in a [Google Drive folder][sheets].

If you want to join my
[private leaderboard](https://adventofcode.com/2022/leaderboards/private), use
the join code: `218680-10f0ed92`

[sheets]: https://drive.google.com/drive/u/0/folders/1ygA0dIsGWcbjLKzuw2XL1Ltr_navxqG4

Setup
-----

1. Clone this repo.
2. From the root of the repo use `python -m venv venv` to create a virtualenv.
3. Use `source venv/bin/activate` to active the virtualenv.
4. Run `pip install -r requirements.txt` to install dependencies.
5. Create a `.env` file `AOC_SESSION_COOKIE=<session cookie>` in it. To find
   your session cookie, log into AoC and in your browser's devtools, find the
   value of the cookie named `session`.

Download input files
--------------------

To download the input for a given day, run
`python download_input.py <year> <day>`. The output will be put in a file named
`<year>/day<day>.txt`.

Using the Python template
-------------------------

The template is broken up into four sections. At the top are a bunch of imports
that are commonly used so you don't have to remember to go import them. The
`get_input` function's job is to read the input from a text file and parse it.
The `part1` and `part2` functions are fed the input (whatever `get_input`
returns) and are expected to return the answer to that part. Lastly is the
section the parses command-line options and calls the other three functions.

Each day, copy `template.py` to `day<day>.py`. By default `get_input` uses the
filename of the script (with `.py` changed to `.txt`) to find the input file.
The first part you should edit is is the last line of `get_input`. The first
four lines of that function read the file. The last line by default just splits
it into lines. But it usually makes sense to do something to parse each line,
like into a tuple of of integers if it was a comma separated list of numbers, or
to parse values out of a regex, or something else.

Next implement the part 1 function. Big caveat here: don't mutate the `input`
that is passed to it! That same input is passed to `part2` and if you change
the input, the `part2` output will be wrong. Do a copy or a deep copy if you
have to. If there is some computation shared between `part1` and `part2` I
recommend adding extra common helper functions.

Running the Python code
-----------------------

For any day, run `python day<day>.py`. With no other arguments it will load the
default input and run parts 1 and 2. To run only one of the parts, pass
`--part1` or `--part2`. `--part2` is especially helpful on days where part 1 is
slow and you want to get the answer to part 2 without having to re-run part 1,
or if you accidentally mutated the input in part 1 and want to run part 2 with
the original input without having to fix part 1 right away. If you want to try
the code on some other input, you can put that other input in a separate file
and pass its name on the command line (but I usually just overwrite the real
input file and then revert it). Lastly, if you use `--clip` it will copy the
last non-null solution to the clipboard so you can paste it directly into the
AoC answer box.

Running the SQLite solutions
----------------------------

Run `sqlite3 < day<day>.sql`. All the SQLite solutions just read the default
`day<day>.txt` input files.


Examples of some techniques
---------------------------

- ASM
  * [2015/day23](2015/day23.py)
  * [2016/day12](2016/day12.py)
  * [2016/day23](2016/day23.py)
  * [2016/day25](2016/day25.py)
  * [2017/day18](2017/day18.py) (mutual recursion)
  * [2017/day23](2017/day23.py)
  * [2018/day16](2018/day16.py)
  * [2018/day19](2018/day19.py)
  * [2018/day21](2018/day21.py)
  * [2019/day2](2019/day2.py) (intcode)
  * [2019/day5](2019/day5.py) (intcode)
  * [2019/day7](2019/day7.py) (intcode)
  * [2019/day9](2019/day9.py) (intcode)
- A*
  * [2015/day19](2015/day19.py)
  * [2015/day22](2015/day22.py)
  * [2016/day13](2016/day13.py)
  * [2016/day17](2016/day17.py)
  * [2016/day22](2016/day22.py)
  * [2016/day24](2016/day24.py)
  * [2018/day22](2018/day22.py)
- BFS
  * [2016/day24](2016/day24.py)
- Union/Find
  * [2017/day14](2017/day14.py)
- Permutations
  * [2015/day9](2015/day9.py)
  * [2015/day13](2015/day13.py)
  * [2016/day24](2015/day24.py)
- Count Bits
  * [2017/day14](2017/day14.py)
- Vector
  * [2017/day20](2017/day20.py)
- Maze
  * [2016/day24](2016/day24.py)
- Skipping Iteration
  * [2018/day12](2018/day12.py)
  * [2018/day18](2018/day18.py)
- Graphical
  * [2018/day13](2018/day13.py)
  * [2018/day15](2018/day15.py)
  * [2018/day17](2018/day17.py)
  * [2018/day18](2018/day18.py)
- Game of Life
  * [2018/day18](2018/day18.py)
