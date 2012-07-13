#!/usr/bin/env python3

import sys
import random


while True:
    heap_sizes = [int(n) for n in input().split(' ')]
    heap_number = random.randrange(len(heap_sizes))
    removed_stones = 1 + heap_sizes[heap_number]
    print(heap_number, removed_stones)
    sys.stdout.flush()
