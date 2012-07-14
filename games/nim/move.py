def deserialize(stream):
    representation = stream.readline().decode()
    heap_number, removed_stones = \
      [int(n) for n in representation.split(' ')]
    return (heap_number, removed_stones)
