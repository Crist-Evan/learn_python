import random

card = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
dice = (1, 2, 3, 4, 5, 6)
mons = {17, 24, 34, 47, 69, 89, 101}

draw = random.randint(card[0], card[len(card) - 1])
mult = random.randint(dice[0], dice[len(dice) - 1])
point = draw * mult

print(f"{draw} * {mult} = {point}")