import random

ids = [1]

def get_next_id():
    id = None
    while id is None and id not in ids:
        id = random.random() * 100
    ids.append(id)
    return int(id)