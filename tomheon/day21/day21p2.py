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


def find_one(allergens_to_candidates):
    for a, c in allergens_to_candidates.items():
        if len(c) == 1:
            return a, c


def map_allergens(allergens_to_ingredients):
    allergens_to_candidates = dict({a: reduce(operator.and_, allergens_to_ingredients[a]) for a in allergens_to_ingredients})
    mapped_allergens = dict()

    while allergens_to_candidates:
        allergen, ingredients = find_one(allergens_to_candidates)
        mapped_allergens[allergen] = list(ingredients)[0]
        del allergens_to_candidates[allergen]
        for a in allergens_to_candidates:
            allergens_to_candidates[a] -= ingredients
                    
    return mapped_allergens
    


def main():
    ingredient_lines = parse_ingredient_lines([line.strip() for line in sys.stdin if line.strip()])
    allergens_to_ingredients = map_ingredients(ingredient_lines)
    mapped_allergens = map_allergens(allergens_to_ingredients)
    tups = list(mapped_allergens.items())
    tups.sort()
    print(','.join([t[1] for t in tups]))

if __name__ == '__main__':
    main()
