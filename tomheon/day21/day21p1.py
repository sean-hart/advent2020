import sys
import re
from collections import defaultdict
from functools import reduce
import operator
from itertools import product


def parse_ingredient_line(line):
    m = re.match(r'^(.+) \(contains (.+)\)', line)
    return m.group(2).split(', '), set(m.group(1).split())
    

def parse_ingredient_lines(lines):
    return [parse_ingredient_line(line) for line in lines]

def map_ingredients(ingredient_entries):
    allergens_to_ingredients = defaultdict(list)
    for (allergens, ingredients) in ingredient_entries:
        for a in allergens:
            allergens_to_ingredients[a].append(ingredients)
    return allergens_to_ingredients


def is_candidate(ingredient, ingredient_lists):
    return all([ingredient in ingredient_list for ingredient_list in ingredient_lists])


def main():
    ingredient_lines = parse_ingredient_lines([line.strip() for line in sys.stdin if line.strip()])
    allergens_to_ingredients = map_ingredients(ingredient_lines)
    all_allergens = allergens_to_ingredients.keys()
    all_ingredients = reduce(operator.or_, [reduce(operator.or_, ingredient_lists) for ingredient_lists in allergens_to_ingredients.values()])
    non_allergens = [i for i in all_ingredients
                     if not any([is_candidate(i, allergens_to_ingredients[allergen]) for allergen in all_allergens])]
    print(sum([na in il[1] for na in non_allergens for il in ingredient_lines]))
    

if __name__ == '__main__':
    main()
