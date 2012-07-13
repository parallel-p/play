def deserialize(stream):
    representation = stream.readline()
    heap_number, removed_stones = \
      [int(n) for n in representation.split(' ')]
    return (heap_number, removed_stones)
