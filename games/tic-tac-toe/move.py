def deserialize(stream):
    return tuple([int(n) \
        for n in stream.readline().decode().split(' ')])
