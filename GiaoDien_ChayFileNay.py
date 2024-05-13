import tkinter as tk
from Astar import *
from Gen_maze import Export_maze
from tkinter import messagebox

def start(entry_boxes,  radio_var_choose_heu,radio_var_gen_maze):
    # Get text from entry widgets
    text_values = [entry.get() for entry in entry_boxes]
    
    # Get selected radio button value
    radio_heu_value = radio_var_choose_heu.get()
    if radio_heu_value == 1:
        heuristics_selection = 'Euclid'
    elif radio_heu_value == 2:
        heuristics_selection = 'Manhattan'
    else:
        heuristics_selection = 'Manhattan'
    
    # Get selected radio button value
    gen_maze_radio_value = radio_var_gen_maze.get()

    # Print entered text and radio button value
    print("Entered Text Values:")
    for i, text in enumerate(text_values):
        print(f"Text Box {i+1}: {text}")
    print(f"Selected Radio Heuristic Button: {heuristics_selection}")
    print(f"Selected Radio Gen Maze Button: {gen_maze_radio_value}")

    rows,cols = [int (x) for x in text_values[0].split(',')]
    if gen_maze_radio_value == 1:
        Export_maze(rows,cols,'Maze.txt',float(text_values[1]))
        grid = Read_maze("Maze.txt")
    elif gen_maze_radio_value == 2:
        grid = Read_maze("Maze.txt")
        rows = len(grid)
        cols = len(grid[0])
    
    if text_values[3] == "Auto":
        start=[rows-1,0]
    else:
        start=[int(x) for x in text_values[3].split(',')]

    if text_values[4] == "Auto":
        dest=[0,cols-1]
    else:
        dest=[int(x) for x in text_values[4].split(',')]
    

    ### Avoid wall in start and dest##
    grid[start[0]][start[1]] = 0
    grid[dest[0]][dest[1]] = 0
    ##############################

    delay = int(text_values[2])


    if is_wall(grid, dest):
        status = "Dest is wall"
    
    elif is_wall(grid, start):
        status = "Start is wall"

    elif out_of_grid(rows, cols, dest):
        status = "Destination is out of grid"
    
    elif out_of_grid(rows, cols, start):
        status = "Start is out of grid"
    
    elif is_destination(start, dest):
        status = "Start is destination: " + str([start])
    else:
        status = Astar(grid,start,dest, delay,heuristics_selection,WIDTH=1350,HEIGHT=650)

    messagebox.showinfo('Status',status)


def main():
    root = tk.Tk()
    root.title("ASTAR")

    # Create entry boxes
    entry_boxes = []
    descriptions = ["SoHang,SoCot(1:2):", "XacSuat:", "Delay(mil):", "Start (ex: 0,0):", "End (ex: 1,1):"]
    for i, desc in enumerate(descriptions):
        label = tk.Label(root, text=desc, font=("Arial", 14))
        label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(root, font=("Arial", 14), width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry_boxes.append(entry)

        # Set default values
    entry_boxes[0].insert(0, '12,24')  # Default Textbox
    entry_boxes[1].insert(0, '0.3')  # Default Textbox
    entry_boxes[2].insert(0, '0')  # Default Textbox
    entry_boxes[3].insert(0, 'Auto')  # Default Textbox
    entry_boxes[4].insert(0, 'Auto')  # Default Textbox
    # entry_boxes[5].insert(0, 'Default Value 1')  # Default Textbox 1
    # entry_boxes[6].insert(0, 'Default Value 2')  # Default Textbox 2
    # entry_boxes[7].insert(0, 'Default Value 3')  # Default Textbox 3

    # Create radio buttons
    radio_var_choose_heu = tk.IntVar()
    radio_var_choose_heu.set(0)  # Set default value to none

    radio_frame = tk.Frame(root)
    radio_frame.grid(row=len(descriptions)  + 1, columnspan=2, padx=10, pady=5)

    radio_Euclid = tk.Radiobutton(radio_frame, text="Euclid", variable=radio_var_choose_heu, value=1, font=("Arial", 14))
    radio_Euclid.grid(row=0, column=0, padx=10)

    radio_Manhattan = tk.Radiobutton(radio_frame, text="Manhattan", variable=radio_var_choose_heu, value=2, font=("Arial", 14))
    radio_Manhattan.grid(row=0, column=1, padx=10)
    radio_Manhattan.select()







    ########################################################################
    radio_var_gen_maze = tk.IntVar()
    radio_var_gen_maze.set(0)  # Set default value to none
    # Create a new frame for the third radio button
    new_radio_frame = tk.Frame(root)
    new_radio_frame.grid(row=len(descriptions), columnspan=2, padx=10, pady=5)

    # Create the third radio button
    radio_gen_maze = tk.Radiobutton(new_radio_frame, text="Gen New Maze", variable=radio_var_gen_maze, value=1, font=("Arial", 14))
    radio_gen_maze.grid(row=0, column=0, padx=10)
    radio_dont_gen_maze = tk.Radiobutton(new_radio_frame, text="Dont Gen New Maze", variable=radio_var_gen_maze, value=2, font=("Arial", 14))
    radio_dont_gen_maze.grid(row=0, column=1, padx=10)
    radio_dont_gen_maze.select()
    #######################################################################




    # Create start button
    start_button = tk.Button(root, text="Start", command=lambda: start(entry_boxes,radio_var_choose_heu,radio_var_gen_maze), font=("Arial", 14))
    start_button.grid(row=len(descriptions) + 2, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
