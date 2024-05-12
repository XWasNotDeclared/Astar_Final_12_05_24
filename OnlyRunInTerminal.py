from PriorityQueue import PriorityQueue
from Heuristic import cal_heuristics

from Gen_maze import random_generate_maze
from Read_maze import Read_maze


#             ]
grid = Read_maze('Maze.txt')

delay_time = 3              # delay time of pygame
rows = len(grid)
cols = len(grid[0])




#################################################




class Cell:
    def __init__(self):
        self.g = float("inf")
        self.f = float("inf")
        self.h = 0.0
        self.parent = [0,0]

def is_wall(grid, cell):
    return grid[cell[0]][cell[1]] == 1

def out_of_grid(grid_row, grid_col, cell):
    return cell[0] < 0 or  cell[0] >= grid_row or  cell[1] < 0 or  cell[1] >= grid_col

def is_destination(cell, dest):
    return cell[0] == dest[0] and cell[1] == dest[1]

def trace_path(grid_infor, start, dest):
    path = []
    current = dest
    while current != start:
        path.append(current)
        current = grid_infor[current[0]][current[1]].parent
    path.append(current)
    path.reverse()

    return len(path)

def detail_cell(grid_infor, cell):
    g = round(grid_infor[cell[0]][cell[1]].g, 2)
    h = round(grid_infor[cell[0]][cell[1]].h, 2)
    f = round(grid_infor[cell[0]][cell[1]].f, 2)
    parent = grid_infor[cell[0]][cell[1]].parent
    return ['g: '+str(g),'h: '+str(h),'f: '+str(f),'par: '+str(parent)]

def length_closed_list(is_close_cell):
    temp=0
    for x in is_close_cell:
        for y in x:
            if y==True:
                temp+=1
    return temp

def Astar(grid,start, dest, num_directional_offset = 8):
    if num_directional_offset == 8:
        cal_distance_method = "Euclid"
        directional_offset = [
            (-1,0), #up
            (1,0),  #down
            (0,-1), #left
            (0,1),  #right
            (-1,-1),#top-left
            (-1,1), #top-right
            (1,-1), #bottom-left
            (1,1),  #bottom-right
        ]

    elif num_directional_offset == 4:
        choose = 2 #int(input("Choose: 1 - Euclid; 2 - Manhattan:  "))
        if choose == 1:
            cal_distance_method = "Euclid"
        elif choose == 2:
            cal_distance_method = "Manhattan"
        directional_offset = [
            (-1,0), #up
            (1,0),  #down
            (0,-1), #left
            (0,1),  #right
        ] 

    GRID_ROW = len(grid)
    GRID_COL = len(grid[1])
    grid_infor = [[Cell() for j in range(GRID_COL)] for i in range(GRID_ROW)]
    grid_infor [start[0]][start[1]].g = 0.0
    grid_infor [start[0]][start[1]].h = cal_heuristics(start,dest,cal_distance_method)
    grid_infor [start[0]][start[1]].f = grid_infor [start[0]][start[1]].g + grid_infor [start[0]][start[1]].h
    is_close_cell = [[False for i in range(GRID_COL)] for j in range(GRID_ROW)]



    if is_wall(grid, dest):
        return "Dest is wall"
    
    if out_of_grid(GRID_ROW, GRID_COL, dest):
        return "Destination is out of grid"
    
    if is_wall(grid, start):
        return "Start is wall"
    
    if out_of_grid(GRID_ROW, GRID_COL, start):
        return "Start is out of grid"
        
    if is_destination(start, dest):
        return "Start is destination: " + str([start])
    

    open_list = PriorityQueue()
    open_list.push((0.0,start)) # add start to open_list with f_start is 0





    while not open_list.isEmpty():


        #print (open_list)
        current_cell = open_list.pop()[1] # get the coordinate of cell with smallest h
        #draw_cell(WIN,current_cell,detail_cell(grid_infor,current_cell),(100,25,70))
        #pygame.time.delay(delay_time)###########################################################
        is_close_cell[current_cell[0]][current_cell[1]] = True # set current_cell is close
        ##print (current_cell)
        #draw_cell(WIN,current_cell,detail_cell(grid_infor, current_cell),blue)
        #draw_cell(WIN,start,detail_cell(grid_infor,start),cyan)

        for direction in directional_offset:
            next_cell = [current_cell[0] + direction[0], current_cell[1] + direction[1]]
            if (not out_of_grid(GRID_ROW, GRID_COL, next_cell)) and (not is_wall(grid,next_cell)) and (not is_close_cell[next_cell[0]][next_cell[1]]) :
                ##print (next_cell)
                if is_destination(next_cell,dest):
                    #draw_cell(WIN,dest,detail_cell(grid_infor,dest),dark_red)
                    grid_infor[next_cell[0]][next_cell[1]].parent = current_cell
                    print("v2" + str(length_closed_list(is_close_cell)))
                    return trace_path(grid_infor, start, dest)
                
                else:
                    g_new_next_cell = grid_infor[current_cell[0]][current_cell[1]].g + 1.0
                    h_new_next_cell = cal_heuristics(next_cell,dest,cal_distance_method)
                    f_new_next_cell = g_new_next_cell + h_new_next_cell
                    ##print((g_new_next_cell, h_new_next_cell, f_new_next_cell))
                    if grid_infor[next_cell[0]][next_cell[1]].f == float("inf") or f_new_next_cell < grid_infor[next_cell[0]][next_cell[1]].f:
                        # add next_cell to open_list or update if it was in open list
                        open_list.push((f_new_next_cell,next_cell))
                        grid_infor[next_cell[0]][next_cell[1]].parent = current_cell
                        grid_infor[next_cell[0]][next_cell[1]].g = g_new_next_cell
                        grid_infor[next_cell[0]][next_cell[1]].h = h_new_next_cell
                        grid_infor[next_cell[0]][next_cell[1]].f = f_new_next_cell
                        # draw next_cell
                        #draw_cell(WIN,next_cell,detail_cell(grid_infor,next_cell),green)

        #pygame.time.delay(delay_time)

    #####return "Cannot finding !!!"
    return -1

if __name__ == "__main__":
        print (Astar(grid, [rows-1,cols-1], [0,0],4))