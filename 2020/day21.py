import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import operator
import os.path
import re
import sys

#import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  foods = []
  for line in input.split('\n'):
    match = re.search(r'^(\w+(?: \w+)*) \(contains (\w+(?:, \w+)*)\)$', line)
    foods.append((set(match.group(1).split(' ')),
                  set(match.group(2).split(', '))))
  return foods


def find_allergens(foods):
  all_ingredients = set()
  allergen_options = {}
  ingredient_allergens = {}
  for ingredients, allergens in foods:
    all_ingredients.update(ingredients)
    for allergen in allergens:
      if allergen in allergen_options:
        allergen_options[allergen] &= set(ingredients)
      else:
        allergen_options[allergen] = set(ingredients)
  found = True
  while found:
    found = False
    for allergen, ingredients in allergen_options.items():
      ingredients -= set(ingredient_allergens.keys())
      if len(ingredients) == 1:
        ingredient = next(iter(ingredients))
        ingredient_allergens[ingredient] = allergen
        found = True
  unknown_ingredients = functools.reduce(operator.or_,
                                         allergen_options.values())
  assert not unknown_ingredients
  safe_ingredients = (all_ingredients - unknown_ingredients
                      - set(ingredient_allergens.keys()))
  for ingredient in safe_ingredients:
    ingredient_allergens[ingredient] = None
  return ingredient_allergens


def part1(input):
  ingredient_allergens = find_allergens(input)
  safe_ingredients = {ingredient
                      for ingredient, allergen in ingredient_allergens.items()
                      if allergen is None}
  return sum(len(ingredients & safe_ingredients) for ingredients, _ in input)


def part2(input):
  ingredient_allergens = find_allergens(input)
  allergen_ingredients = {
      allergen: ingredient
      for ingredient, allergen in ingredient_allergens.items()
      if allergen is not None
  }
  return ','.join(ingredient
                  for _, ingredient in sorted(allergen_ingredients.items()))


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
