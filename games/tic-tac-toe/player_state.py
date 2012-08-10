def serialize(ps, stream):
    stream.write('\n'.join([' '.join([j \
                            for j in ps.field[i * 3:(i + 1) * 3]]) \
                            for i in range(3)]).encode())
    stream.flush()


class PlayerState:
    def __init__(self, field):
        self.field = field
