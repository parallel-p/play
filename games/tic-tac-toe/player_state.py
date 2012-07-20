def serialize(field, stream):
    stream.write('\n'.join([' '.join([j \
        for j in field[i * 3:(i + 1) * 3]]) for i in range(3)]).encode())
    stream.flush()
