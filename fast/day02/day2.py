with open('input') as f:
    lines = f.readlines()

depth = 0
hor = 0
aim = 0
for line in lines:
    dir, m = line.strip().split()
    m = int(m)
    if dir == 'forward':
        hor += m
        depth += (aim*m)
    elif dir == 'down':
        aim += m
    elif dir == 'up':
        aim -= m

print(depth, hor, aim, depth*hor)
