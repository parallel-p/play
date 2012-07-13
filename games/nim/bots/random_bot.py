#!/usr/bin/env python3

import sys
import random


while True:
    heap_sizes = [int(n) for n in input().split(' ')]
    allowed = [i for i, size in enumerate(heap_sizes) if size > 0]
    heap_number = random.choice(allowed)
    removed_stones = random.randint(1, heap_sizes[heap_number])
    print(heap_number, removed_stones)
    sys.stdout.flush()
