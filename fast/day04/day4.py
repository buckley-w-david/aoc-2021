#!/usr/bin/python

with open('input') as f:
    lines = f.read()

blocks = lines.split("\n\n")
draws = [int(i) for i in blocks[0].split(',')]

boards = []
for block in blocks[1:]:
    lines = [i.strip().split() for i in block.split("\n") if i]
    boards.append([[[ int(i), False ] for i in j] for j in lines])

def winner():
    for draw in draws:
        for board in boards:
            for row in board:
                for cell in row:
                    if cell[0] == draw:
                        cell[1] = True
        remove = []
        for i, board in enumerate(boards):
            for row in board:
                if all([cell[1] for cell in row]):
                    if len(boards) == 1:
                        return (board, draw)
                    else:
                        remove.append(board)
            for col_idx in range(len(board[0])):
                if all([row[col_idx][1] for row in board]):
                    if len(boards) == 1:
                        return (board, draw)
                    else:
                        remove.append(board)

        for board in remove:
            try:
                boards.remove(board)
            except ValueError:
                pass

board, draw = winner()
s = 0
for row in board:
    for cell in row:
        if not cell[1]:
            s += cell[0]

print(s * draw)
