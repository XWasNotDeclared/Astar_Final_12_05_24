def Euclidean_Distance(cell, dest):
    return ((cell[0] - dest[0])**2 + (cell[1] - dest[1])**2)**0.5

def Manhattan_Distance(cell, dest):
    return abs(cell[0] - dest[0]) + abs(cell[1] - dest[1])

def cal_heuristics(cell, dest, cal_distance_method):
    if cal_distance_method == "Manhattan":
        return Manhattan_Distance(cell, dest)
    elif cal_distance_method == "Euclid":
        return Euclidean_Distance(cell, dest)
    