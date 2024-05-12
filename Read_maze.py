def Read_maze(filename):
    maze = []
    with open(filename,'r') as file:
        line = file.readline()
        while line:
            row = [int(x) for x in line.strip().split()]
            maze.append(row)
            line = file.readline()
    return maze

if __name__ == '__main__':
    print (Read_maze("Maze.txt"))