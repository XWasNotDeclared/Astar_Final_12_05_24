import random

def random_generate_maze(rows, cols, wall_possibilities):
    # 1 is blocked
    maze = [[1 if random.random() < wall_possibilities else 0 for _ in range(cols)] for _ in range(rows) ]

    # maze[0][0] = 0
    # maze[len(maze)-1][len(maze[0])-1] = 0

    return maze

def Export_maze(rows, cols,filename = 'Maze.txt', wall_possibilities = 0.1):
    maze = random_generate_maze(rows, cols, wall_possibilities)
    rows = len(maze)
    cols = len(maze[1])
    
    with open(filename, 'w') as file:
        for row in range(rows):
            for col in range(cols):
                file.write(str(maze[row][col]) + ' ')
            file.write('\n')

if __name__ == '__main__':
    Export_maze(10,10,'Maze.txt',0.3)
