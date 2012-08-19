def deserialize(stream):
    return [int(n) for n in stream.readline().decode().split()]
