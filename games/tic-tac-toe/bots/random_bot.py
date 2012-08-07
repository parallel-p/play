import sys
import random

field = [['.' for i in range(3)] for j in range(3)]
for i in range(3):
    row = sys.stdin.readline().split()
    for j, element in enumerate(row):
        field[i][j] = element

random.seed()
while True:
    i = random.randint(0, 2)
    j = random.randint(0, 2)
    if field[i][j] == '.':
        print(i + 1, j + 1)
        sys.stdout.flush()
        break
