#!/usr/bin/env python

import argparse
import os
import os.path
import time

import dotenv
import requests


def download_input(year, day, session_cookie):
  url = f'https://adventofcode.com/{year}/day/{day}/input'
  cookies = {'session': session_cookie}
  response = requests.get(url, stream=True, cookies=cookies)
  response.raise_for_status()
  filename = os.path.join(os.path.dirname(__file__), f'{year}/day{day}.txt')
  with open(filename, 'wb') as fp:
    for chunk in response.iter_content(None):
      fp.write(chunk)


if __name__ == '__main__':
  dotenv.load_dotenv()

  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--session-cookie', '--cookie')
  parser.add_argument('-r', '--retries', type=int, default=5,
                      help='Number of retries')
  parser.add_argument('-d', '--retry-delay', type=float, default=1,
                      help='Seconds to delay between retries')
  parser.add_argument('year', type=int)
  parser.add_argument('day', type=int)
  args = parser.parse_args()

  if not args.session_cookie:
    args.session_cookie = os.getenv('AOC_SESSION_COOKIE')

  if not args.session_cookie:
    parser.error(
        'Must set session cookie with -c or AOC_SESSION_COOKIE env var')

  for i in range(args.retries):
    if i > 0:
      time.sleep(args.retry_delay)
    try:
      download_input(args.year, args.day, args.session_cookie)
    except requests.HTTPError as e:
      print(f'Not ready yet: {e}')
    else:
      break
  else:
    raise SystemExit('timed out after limit of retry attempts')
