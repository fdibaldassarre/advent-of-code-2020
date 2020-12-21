#!/usr/bin/env python3


class Food:

    def __init__(self, ingredients, allergens):
        self.ingredients = ingredients
        self.allergens = allergens


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def read_food_list():
    food_list = list()
    for line in read_input():
        if "(contains" in line:
            ingredients_raw, allergens_raw = line.split(" (contains ")
            allergens_raw = allergens_raw[:-1]
        else:
            ingredients_raw, allergens_raw = line, None
        ingredients = set(ingredients_raw.split(" "))
        if allergens_raw is not None:
            allergens = set(allergens_raw.split(", "))
        else:
            allergens = set()
        food_list.append(Food(ingredients, allergens))
    return food_list


def compute_alergens_to_ingredients(food_list):
    # Map alergen to possible ingredients
    allergen_to_ingredients = dict()
    for food in food_list:
        for allergen in food.allergens:
            if allergen not in allergen_to_ingredients:
                allergen_to_ingredients[allergen] = set(food.ingredients)
            else:
                allergen_to_ingredients[allergen] = allergen_to_ingredients[allergen].intersection(food.ingredients)
    return allergen_to_ingredients


def solve1(food_list, allergen_to_ingredients):
    # Find all the ingredients that may be alergens
    ingredients_with_possible_alergens = set()
    for ingredients in allergen_to_ingredients.values():
        ingredients_with_possible_alergens = ingredients_with_possible_alergens.union(ingredients)
    # Count the number of non-alergen ingredients
    non_alergens_usages = 0
    for food in food_list:
        for ingredient in food.ingredients:
            if ingredient not in ingredients_with_possible_alergens:
                non_alergens_usages += 1
    return non_alergens_usages


def solve2(allergen_to_ingredients):
    ingredient_to_allergen = dict()
    while True:
        ingredient_to_allergen_update = dict()
        for allergen, possible_ingredients in allergen_to_ingredients.items():
            if len(possible_ingredients) == 1:
                ingredient = list(possible_ingredients)[0]
                ingredient_to_allergen_update[ingredient] = allergen
        # Cleanup
        allergen_resolved = set(ingredient_to_allergen_update.values())
        if len(allergen_resolved) == 0:
            break
        for allergen in allergen_resolved:
            del allergen_to_ingredients[allergen]
        # Remove from the possibilities
        ingredients_resolved = set(ingredient_to_allergen_update.keys())
        for allergen, possible_ingredients in allergen_to_ingredients.items():
            possible_ingredients.difference_update(ingredients_resolved)
        # Update
        ingredient_to_allergen.update(ingredient_to_allergen_update)
    dangerous_ingredients = sorted(ingredient_to_allergen.keys(), key=lambda ingredient: ingredient_to_allergen[ingredient])
    return ",".join(dangerous_ingredients)


if __name__ == "__main__":
    food_list = read_food_list()
    allergen_to_ingredients = compute_alergens_to_ingredients(food_list)
    solution1 = solve1(food_list, allergen_to_ingredients)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(allergen_to_ingredients)
    print("Solution 2: %s" % solution2)
