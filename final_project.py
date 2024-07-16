import random
import time
import tkinter as tk
from tkinter import font
import sweeperlib

state = {
    "start_time": -1,
    "end_time": 0,
    "field": [],
    "available_tiles": None,
    "mine_numbers": 0,
    "available_mines": [],
    "result": [],
    "height": 0,
    "width": 0,
}

def place_mines(
    fields_to_mine: list[list[str]],
    available_tiles: list[tuple[int, int]],
    mine_numbers: int,
) -> None:
    """
    Places N mines to a field in random tiles.
    """

    mined_tiles = random.sample(available_tiles, mine_numbers)

    for x_coordinate, y_coordinate in mined_tiles:
        state["available_mines"].append((y_coordinate, x_coordinate))
        fields_to_mine[y_coordinate][x_coordinate] = 'x'
        state["available_tiles"].remove((x_coordinate, y_coordinate))
    
    return fields_to_mine

def place_numbers(field) -> None:
    """
    Places the valid numbers of the generated board
    """
    rows = len(field)
    cols = len(field[0])

    for i in range(rows):
        for j in range(cols):
            tile_mine_count = 0
            if field[i][j] == "x":
                continue

            # Check adjacent tiles
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    new_x = i + dx
                    new_y = j + dy

                    # Make sure new coordinates are within bounds
                    if 0 <= new_x < rows and 0 <= new_y < cols:
                        neighbor_tile = field[new_x][new_y]

                    # Checking if the adjacent tiles have a mine
                        if neighbor_tile == "x":
                            tile_mine_count += 1
            field[i][j] = str(tile_mine_count)

def draw_field() -> None:
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()

    for i, row in enumerate(state["field"]):
        for j, key in enumerate(row):
            sweeperlib.prepare_sprite(key, (j) * 40, (state["height"] - i - 1) * 40)

    sweeperlib.draw_sprites()

def open_tile(x, y, button, mods):
    """
    Checks the state of the tile clicked on, whether it has a mine or not
    """
    if state["start_time"] == -1:
        state["start_time"] = time.time()
    button_names = {
        sweeperlib.MOUSE_LEFT: "left",
        sweeperlib.MOUSE_RIGHT: "right"
    }
    button_name = button_names.get(button, "unknown")

    # kiem tra coi no la click chuot phai hay chuot trai
    x_corendation = state["height"] - 1 - y // 40
    # state["height"] - i - 1
    y_corendation = x // 40
    if (button_name == 'left'):
        if state['field'][x_corendation][y_corendation] != " ":
            return
        # dựa vào x, y
        # kiểm tra ô đó là mìn => loss screen
        
        # kiểm tra nếu là ô 1, 2, 3,... => hiển thị ô đó.
        if (state["result"][x_corendation][y_corendation] == "x"):
            for mine_x, mine_y in state["available_mines"]:
                state["field"][mine_x][mine_y] = state["result"][mine_x][mine_y]
            # Go to loss screen
        elif((int(state["result"][x_corendation][y_corendation])) in [1, 2, 3, 4, 5, 6, 7, 8]):
            state["field"][x_corendation][y_corendation] = state["result"][x_corendation][y_corendation]
            state['available_tiles'].remove((y_corendation, x_corendation))
        elif (state["result"][x_corendation][y_corendation] != "x"):
            floodfill(x_corendation, y_corendation)
        
        # Kiểm tra nếu là empty => thực hiện floodfill
        
        
    elif (button_name == 'right'):
        if state["field"][x_corendation][y_corendation] != " " and state["field"][x_corendation][y_corendation] != "f":
            return
        if state["field"][x_corendation][y_corendation] == " ":
            state["field"][x_corendation][y_corendation] = "f"
        elif state["field"][x_corendation][y_corendation] == "f":
            state["field"][x_corendation][y_corendation] = " "

    if len(state["available_tiles"]) == 0:
        for mine_x, mine_y in state["available_mines"]:
            state["field"][mine_x][mine_y] = "f"
        won_title_label.pack()
        try_again_button.pack()

    sweeperlib.set_draw_handler(draw_field)

def main() -> None:
    """
    Loads the game graphics, creates a game window and sets a draw handler for it.
    """
    sweeperlib.load_sprites('./sprites')
    sweeperlib.create_window(40 * state["width"], 40 * state["height"])
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.set_mouse_handler(open_tile)

    sweeperlib.start()


def floodfill(x_coordinate: int, y_coordinate: int) -> None:
    """
    Marks previously unknown connected areas as safe, starting from the given x, y coordinates.
    """
    unvisited_tile = [(x_coordinate, y_coordinate)]
    visited_tile = []

    while len(unvisited_tile) > 0:
        visited_x_coordinate, visited_y_coordinate = unvisited_tile.pop()
        if ((visited_x_coordinate, visited_y_coordinate) not in visited_tile):
            state["field"][visited_x_coordinate][visited_y_coordinate] = state["result"][visited_x_coordinate][visited_y_coordinate]
            if ((visited_y_coordinate, visited_x_coordinate) in state["available_tiles"]):
                state['available_tiles'].remove((visited_y_coordinate, visited_x_coordinate))
            if state["result"][visited_x_coordinate][visited_y_coordinate] == 'x' or int(state["result"][visited_x_coordinate][visited_y_coordinate]) in [1, 2, 3, 4, 5, 6, 7, 8]:
                continue
            visited_tile.append((visited_x_coordinate, visited_y_coordinate))
            
            height = len(state["field"])
            width = len(state["field"][0])
            
            for func_x_1 in [-1, 0, 1]:
                for func_y_1 in [-1, 0, 1]:
                    new_func_x = visited_x_coordinate + func_x_1
                    new_func_y = visited_y_coordinate + func_y_1
                    
                    if 0 <= new_func_x < height and 0 <= new_func_y < width:
                        unvisited_tile.append((new_func_x, new_func_y))

def init(height, width, number_of_mines):
    """
    Generatets the playing field's dimensions and mine count
    """
    for row in range(height):
        state["field"].append([])
        for col in range(width):
            state["field"][row].append(" ")

    for row in range(height):
        state["result"].append([])
        for col in range(width):
            state["result"][row].append(" ")

    # setup available_tiles
    available = []
    for x in range(width):
        for y in range(height):
            available.append((x, y))
    state["available_tiles"] = available
    state["height"] = height
    state["width"] = width

    # init fields with mines
    state["result"] = place_mines(state["result"], available, number_of_mines)
    place_numbers(state["result"])
    # draw and start
    main()

def play_button_click():
    """
    When the "Play" button is pressed:
    """
    play_button.forget()
    statistics_button.forget()
    quit_button.forget()
    opening_title_label.forget()
    show_new_text()
    show_additional_buttons()

def show_additional_buttons():
    """
    The scene after the "Play" button is pressed:
    """
    easy_button.pack(pady = 40)
    normal_button.pack(pady = 40)
    hard_button.pack(pady = 40)
    custom_button.pack(pady = 40)
    back_button.pack(anchor = "sw")

def back_button_click():
    """
    After the "Back" button is pressed:
    """
    easy_button.forget()
    normal_button.forget()
    hard_button.forget()
    custom_button.forget()
    back_button.forget()
    choose_diff_label.forget()
    opening_title_label.pack()
    play_button.pack(pady = 60)
    statistics_button.pack(pady = 60)
    quit_button.pack(pady = 60)

def show_new_text():
    """
    
    """
    choose_diff_label.pack()

def statistics_button_click():
    pass

def quit_button_click():
    quit_program()

def easy_button_click():
    # choose_diff_label.forget()
    # easy_button.forget()
    # normal_button.forget()
    # hard_button.forget()
    # custom_button.forget()
    # back_button.forget()
    init(9, 9, 10)
    


def normal_button_click():
    choose_diff_label.forget()
    easy_button.forget()
    normal_button.forget()
    hard_button.forget()
    custom_button.forget()
    back_button.forget()
    init(16, 16, 40)

def hard_button_click():
    choose_diff_label.forget()
    easy_button.forget()
    normal_button.forget()
    hard_button.forget()
    custom_button.forget()
    back_button.forget()
    init(16, 30, 99)

def custom_button_click():
    choose_diff_label.forget()
    easy_button.forget()
    normal_button.forget()
    hard_button.forget()
    custom_button.forget()
    back_button.forget()
    init(16, 30, 99)

def try_again_button_click():
    lost_title_label.forget()
    won_title_label.forget()
    try_again_button.forget()
    show_new_text()
    show_additional_buttons()
    

def quit_program():
    window.destroy()

# Create the main window
window = tk.Tk()
# window.configure(bg = "#ffffff")

# Set the window to fullscreen
# window.attributes("-fullscreen", True)

width = window.winfo_screenwidth()
height = window.winfo_screenheight()

# Create an entry widget for number input
entry_font = font.Font(size = 20)  # Adjust the font size to change the height
entry = tk.Entry(window, font = entry_font)

# Set the title
window.title("Minesweeper")

# Create a label for the title
opening_title_font = font.Font(family = "Arial", size = 100, weight = "bold")
opening_title_label = tk.Label(window, text = "Minesweeper", font = opening_title_font)
opening_title_label.pack()

# Create Play button
play_button = tk.Button(window, text = "Play", font = ("Arial", 24), width = int(width * 0.02), height = int(height * 0.002), command = play_button_click, bg = '#ffffff', fg = '#000000')
play_button.pack(pady = 60)

# Create Statistics button
statistics_button = tk.Button(window, text = "Statistics", font = ("Arial", 24), width = int(width * 0.02), height = int(height * 0.002), command = statistics_button_click, bg = '#ffffff', fg = '#000000')
statistics_button.pack(pady = 60)

# Create Quit button
quit_button = tk.Button(window, text = "Quit", font = ("Arial", 24), width = int(width * 0.02), height = int(height * 0.002), command = quit_button_click, bg = '#ffffff', fg = '#000000')
quit_button.pack(pady = 60)

# Create OK button
ok_button = tk.Button(window, text = "OK", font = ("Arial", 24), width = int(width * 0.02), height = int(height * 0.002))

# Create Easy button
easy_button = tk.Button(window, text = "Easy (9x9 board, 10 mines)", font = ("Arial", 24), width = int(width * 0.02), height = int(height * 0.002), command = easy_button_click, bg = '#a6f692', fg = '#000000')

# Create Normal button
normal_button = tk.Button(window, text = "Normal (16x16 board, 40 mines)", font = ("Arial", 24), width = int(width * 0.02), height = int(height * 0.002), command = normal_button_click, bg = '#fbdf8c', fg = '#000000')

# Create Hard button
hard_button = tk.Button(window, text = "Hard (16x30 board, 99 mines)", font = ("Arial", 24), width = int(width * 0.02), height = int(height * 0.002), command = hard_button_click, bg = '#ff89b8', fg = '#000000')

# Create Custom button
custom_button = tk.Button(window, text = "Custom", font = ("Arial", 24), width = int(width * 0.02), height = int(height*0.002), bg = '#f383cb', fg = '#000000')

# Create Back button
back_button = tk.Button(window, text = "Back", font = ("Arial", 18), width = int(width * 0.01), height = int(height*0.001), command = back_button_click, bg = '#ffffff', fg = '#000000')

# Create a new text label (hidden initially)
choose_diff_font = font.Font(family = "Arial", size = 60, weight = "bold")
choose_diff_label = tk.Label(window, text = "Choose difficulty", font = choose_diff_font)

# Lost title
lost_title_font = font.Font(family = "Arial", size = 100, weight = "bold")
lost_title_label = tk.Label(window, text = "You lost!", font = lost_title_font)

# Won title
won_title_font = font.Font(family = "Arial", size = 100, weight = "bold")
won_title_label = tk.Label(window, text = "You won!", font = lost_title_font)

# Try again button
try_again_button = tk.Button(window, text = "Try again", font = ("Arial", 24), width = int(width*0.02), height = int(height*0.002), command = try_again_button_click, bg = '#ffffff', fg = '#000000')

# Start the main event loop
window.mainloop()