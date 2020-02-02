import math

def cartesian_distance(x1, x2, y1, y2):
    x_distance = (x2-x1)**2
    y_distance = (y2-y1)**2
    xy_distance = x_distance + y_distance
    return math.sqrt(xy_distance)

nodos = {
    1: (20, 6),
    2: (22, 1),
    3: (9, 2),
    4: (3, 25),
    5: (21, 10),
    6: (29, 2),
    7: (14, 12),
}

arcos = {}

for i in nodos.keys():
    for j in nodos.keys():
        coords_1 = nodos[i]
        coords_2 = nodos[j]
        dist = cartesian_distance(coords_1[0], coords_2[0], coords_1[1], coords_2[1])
        if  0 < dist <= 20:
            arcos[(i, j)] = dist