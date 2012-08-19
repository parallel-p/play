def serialize_field_side(field_side, stream):
    representation = str(field_side) + '\n'
    stream.write(representation.encode())
    stream.flush()


def list_to_str(lst):
    return ' '.join(map(str, lst))


def list_of_tuples_to_strings(lst):
    tuples = [list_to_str([elem[0], elem[1]]) for elem in lst]
    return '\n'.join([list_to_str([len(lst)])] +
                     ['\n'.join(tuples)])


def serialize(ps, stream):
    representation = '\n'.join([
        list_to_str([len(ps.ships)]),

    ])
        [list_to_str([len(ps.ships)])] +
        ['\n'.join([list_of_tuples_to_strings(ship) for ship in ps.ships])]
    )
    stream.write(representation.encode())
    stream.flush()


class PlayerState:
    def __init__(self, field_side, ships):
        self.field_side = field_side
        self.ships = ships
