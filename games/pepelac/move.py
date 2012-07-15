class DeserializeMoveException(Exception):
    pass

def deserialize(stream):
    representation = stream.readline().decode().rstrip()
    dx = [0, 0, 0, 1, -1]
    dy = [0, 1, -1, 0, 0]
    turns = ['STAND', 'RIGHT', 'LEFT', 'DOWN', 'UP']
    answer = None
    for idx, turn in enumerate(turns):
        if turn == representation:
            answer = (dx[idx], dy[idx])
    if answer is None:
        raise DeserializeMoveException("Incorrect move!")
    return answer