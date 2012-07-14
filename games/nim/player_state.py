def serialize(heap_sizes, stream):
    representation = ' '.join([str(n) for n in heap_sizes]) + '\n'
    stream.write(representation.encode())
    stream.flush()
