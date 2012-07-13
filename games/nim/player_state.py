def serialize(self, heap_sizes, stream):
    stream.write(' '.join([str(n) for n in heap_sizes]) + '\n')
    stream.flush()
