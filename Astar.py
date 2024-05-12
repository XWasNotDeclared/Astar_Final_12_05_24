from PriorityQueue import PriorityQueue
from Heuristic import cal_heuristics
import pygame
from Gen_maze import random_generate_maze
from Read_maze import Read_maze
# 1 is blocked
# grid = [    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
#             [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
#             [0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
#             [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
#             [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
#             [0, 1, 0, 0, 0, 0, 1, 0, 1, 1],
#             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
#             [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
#             [0, 0, 0, 1, 1, 1, 0, 1, 1, 0]
#             ]
white = (255,255,255)
black = (0,0,0)
cyan  = (0,255,229) # start color
red   = (255,0,0)   # dest color
blue  = (0,8,255)   # close color
green = (0, 173, 133)  # open color
yellow= (245,255,0) #path color
dark_red = (125,0,0)
light_red = (171, 7, 168) #curent cell color
gray = (217, 216, 212) #gray

def draw_maze(WIN, maze,cell_size):
    rows = len(maze)
    cols = len(maze[0])
    for row in range(rows):
        for col in range(cols):
            if maze[row][col] == 1:
                color = black
            else:
                color = white
            pygame.draw.rect(WIN,color,(col*cell_size,row*cell_size,cell_size,cell_size),0)

def draw_cell(WIN,cell_size, cell_coord, text, bg_color, text_color = gray):
    text_size = int(cell_size*9/35)
    Font = pygame.font.Font(None,text_size)
    pygame.draw.rect(WIN, bg_color, (cell_coord[1]*cell_size, cell_coord[0]*cell_size, cell_size, cell_size),0)
    for i,item in enumerate(text):
        ##
        text_surface = Font.render(item,True,text_color)
        text_position = (cell_coord[1]*cell_size, cell_coord[0]*cell_size + i*text_size)
        WIN.blit (text_surface, text_position)



    # ##
    # text_surface = Font.render(text[0],True,text_color)
    # text_position = (cell_coord[1]*cell_size, cell_coord[0]*cell_size)
    # WIN.blit (text_surface, text_position)
    # ##
    # text_surface = Font.render(text[1],True,text_color)
    # text_position = (cell_coord[1]*cell_size, cell_coord[0]*cell_size + text_size)
    # WIN.blit (text_surface, text_position)
    # ##
    # text_surface = Font.render(text[2],True,text_color)
    # text_position = (cell_coord[1]*cell_size, cell_coord[0]*cell_size + 2*text_size)
    # WIN.blit (text_surface, text_position)
    # ##
    # text_surface = Font.render(text[3],True,text_color)
    # text_position = (cell_coord[1]*cell_size, cell_coord[0]*cell_size + 3*text_size)
    # WIN.blit (text_surface, text_position)


    pygame.display.update((cell_coord[1]*cell_size, cell_coord[0]*cell_size, cell_size, cell_size))



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

def trace_path(WIN,cell_size,grid_infor, start, dest):
    path = []
    current = dest
    while current != start:
        path.append(current)
        current = grid_infor[current[0]][current[1]].parent
    path.append(current)
    path.reverse()
    ##pygame##
    for cell in path:
        draw_cell(WIN,cell_size,cell,detail_cell(grid_infor,cell),yellow)

    draw_cell(WIN,cell_size,start,detail_cell(grid_infor,start),cyan)
    draw_cell(WIN,cell_size,dest,detail_cell(grid_infor,dest),dark_red)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

                
    #########
    return len(path)

def length_closed_list(is_close_cell):
    temp=0
    for x in is_close_cell:
        for y in x:
            if y==True:
                temp+=1
    return temp

def detail_cell(grid_infor, cell):
    g = round(grid_infor[cell[0]][cell[1]].g, 2)
    h = round(grid_infor[cell[0]][cell[1]].h, 2)
    f = round(grid_infor[cell[0]][cell[1]].f, 2)
    parent = grid_infor[cell[0]][cell[1]].parent
    return ["[g,h,f]",str([g,h,f]),"par: ",str(parent),]
    # return ['g: '+str(g),'h: '+str(h),'f: '+str(f),'par: '+str(parent)]

def cal_cell_size(grid,width,height):
    rows = len(grid)
    cols = len(grid[0])
    return  min(width//cols, height//rows)


def Astar(grid,start, dest,delay_time,chooseHeuristic,WIDTH = 1350,HEIGHT=650, num_directional_offset = 4 ):
    pygame.init()

    GRID_ROW = len(grid)
    GRID_COL = len(grid[0])

    # rows = len(grid)
    # cols = len(grid[0])

    cell_size = cal_cell_size(grid,WIDTH,HEIGHT)
    WIDTH = cell_size*GRID_COL
    HEIGHT = cell_size*GRID_ROW

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A star")




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
        cal_distance_method = chooseHeuristic
        directional_offset = [
            (-1,0), #up
            (1,0),  #down
            (0,-1), #left
            (0,1),  #right
        ] 

    if is_wall(grid, dest):
        return "Dest is wall"
    
    if out_of_grid(GRID_ROW, GRID_COL, dest):
        return "Destination is out of grid"
    
    if out_of_grid(GRID_ROW, GRID_COL, start):
        return "Start is out of grid"


    if is_wall(grid, start):
        return "Start is wall"
    
    if is_destination(start, dest):
        return "Start is destination: " + str([start])

    grid_infor = [[Cell() for j in range(GRID_COL)] for i in range(GRID_ROW)]
    grid_infor [start[0]][start[1]].g = 0.0
    grid_infor [start[0]][start[1]].h = cal_heuristics(start,dest,cal_distance_method)
    grid_infor [start[0]][start[1]].f = grid_infor [start[0]][start[1]].g + grid_infor [start[0]][start[1]].h
    is_close_cell = [[False for i in range(GRID_COL)] for j in range(GRID_ROW)]


    

    open_list = PriorityQueue()
    open_list.push((0.0,start)) # add start to open_list with f_start is 0


    draw_maze(WIN,grid,cell_size)
    pygame.display.update()
    draw_cell(WIN,cell_size,start,detail_cell(grid_infor,start),cyan)
    draw_cell(WIN,cell_size,dest,detail_cell(grid_infor,dest),red)

    running = True
    while not open_list.isEmpty() and running:
        ##pygame###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        ###########


        #print (open_list)
        current_cell = open_list.pop()[1] # get the coordinate of cell with smallest h
        draw_cell(WIN,cell_size,current_cell,detail_cell(grid_infor,current_cell),light_red)
        pygame.time.delay(delay_time)###########################################################
        is_close_cell[current_cell[0]][current_cell[1]] = True # set current_cell is close
        ##print (current_cell)
        draw_cell(WIN,cell_size,current_cell,detail_cell(grid_infor, current_cell),blue)
        draw_cell(WIN,cell_size,start,detail_cell(grid_infor,start),cyan)

        for direction in directional_offset:
            next_cell = [current_cell[0] + direction[0], current_cell[1] + direction[1]]
            if (not out_of_grid(GRID_ROW, GRID_COL, next_cell)) and (not is_wall(grid,next_cell)) and (not is_close_cell[next_cell[0]][next_cell[1]]) :
                ##print (next_cell)
                if is_destination(next_cell,dest):
                    draw_cell(WIN,cell_size,dest,detail_cell(grid_infor,dest),dark_red)
                    grid_infor[next_cell[0]][next_cell[1]].parent = current_cell
                    len_path = trace_path(WIN,cell_size,grid_infor, start, dest)

                    return "Success!!!\nLengthPath: " + str(len_path) + "\nClosed cell:" + str(length_closed_list(is_close_cell))
                
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
                        draw_cell(WIN,cell_size,next_cell,detail_cell(grid_infor,next_cell),green)

        # pygame.time.delay(delay_time)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

    return "Can finding !!!\nClosed cell:" + str(length_closed_list(is_close_cell))




if __name__ == "__main__":
        pass