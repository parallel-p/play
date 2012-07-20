#!/usr/bin/env python3

import sys
import random
import operator
from functools import reduce


while True:
    heap_sizes = [int(n) for n in input().split(' ')]
    global_xor = reduce(operator.xor, heap_sizes)
    if global_xor != 0:
        for heap_number, size in enumerate(heap_sizes):
            new_size = global_xor ^ size
            if size > new_size:
                print(heap_number, size - new_size)
                break
    else:
        # Random move
        allowed = [i for i, size in enumerate(heap_sizes) if size > 0]
        heap_number = random.choice(allowed)
        removed_stones = random.randint(1, heap_sizes[heap_number])
        print(heap_number, removed_stones)
    sys.stdout.flush()
