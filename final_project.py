import json
import random
import time
import tkinter as tk
from tkinter import font, simpledialog, messagebox
import sweeperlib

class Table:
     
    def __init__(self, root, lst):
        total_rows = len(lst)
        total_columns = len(lst[0])

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                if i == 0:
                    if j == 0:
                        self.e = tk.Entry(root, width=20, fg='#a6f692',
                                    font=('Arial', 16, 'bold'))
                    elif j == 1: 
                        self.e = tk.Entry(root, width=20, fg='#a6f692',
                                    justify = 'center', font=('Arial', 16, 'bold'))
                        # print('j = 1')
                    elif j == 2:
                        self.e = tk.Entry(root, width=20, fg='#fbdf8c',
                                    justify = 'center', font=('Arial', 16, 'bold'))
                        # print('j = 2')
                    elif j == 3:
                        self.e = tk.Entry(root, width=20, fg='#ff89b8',
                                    justify = 'center', font=('Arial', 16, 'bold'))
                        # print('j = 3')
                else:
                    if j == 0:
                        self.e = tk.Entry(root, width=20, fg='#000000',
                                    font=('Arial', 16, 'bold'))
                        # print('j = 0')
                    else:
                        self.e = tk.Entry(root, width=20, fg='blue',
                                    justify = 'center', font=('Arial', 16))
                        # print('rest')
                        
                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, lst[i][j])

class Constants: 
    DIFFICULTY_LEVELS = {
        "Easy": (9, 9, 10),
        "Medium": (16, 16, 40),
        "Hard": (16, 30, 99),
        "Custom": None
    }
    GAME_STATUS = {
        "Not started": 0,
        "In progress": 1,
        "Paused": 2,
        "Lost": 3,
        "Won": 4
    }
    GAME_ENTRY = {
        "MINE": "x",
        "EMPTY": " ",
        "FLAG": "f"
    }

    GAME_CONFIG = {
        "SIZE_OF_TILE": 40,
        "HEIGHT_OF_BOARD": 50,
    }

class GameState:
    def __init__(self):
        self.start_time = -1
        self.end_time = 0
        self.field = []
        self.available_tiles = None
        self.mine_numbers = 0
        self.available_mines = []
        self.result = []
        self.height = 0
        self.width = 0
        self.current_time = 0
        self.difficulty = None

class MinesweeperGame:
    DIFFICULTY_LEVELS = {
        "Easy": (9, 9, 10),
        "Medium": (16, 16, 40),
        "Hard": (16, 30, 99),
        "Custom": None
    }

    def __init__(self):
        self.state = GameState()
        self.window = None
        self.setup_window()

    def setup_window(self):
        self.window = tk.Tk()
        self.window.resizable(0, 0)
        self.window.title("Minesweeper")
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.setup_fonts()
        self.create_widgets()

    def setup_fonts(self):
        self.opening_title_font = font.Font(family="Arial", size=100, weight="bold")
        self.choose_diff_font = font.Font(family="Arial", size=60, weight="bold")
        self.button_font = font.Font(family="Arial", size=24)

    def create_widgets(self):
        self.opening_title_label = tk.Label(self.window, text="Minesweeper", font=self.opening_title_font)
        self.choose_diff_label = tk.Label(self.window, text="Choose difficulty", font=self.choose_diff_font)
        self.play_button = self.create_button("Play", self.play_button_click)
        self.statistics_button = self.create_button("Statistics", self.statistics_button_click)
        self.reset_button = self.create_button("Clear Cache", self.reset_button_click, font_size=18, width_factor=0.01, height_factor=0.001)
        self.quit_button = self.create_button("Quit", self.quit_program)
        
        self.difficulty_buttons = {}
        colors = ['#a6f692', '#fbdf8c', '#ff89b8', '#f383cb']
        for i, (diff, params) in enumerate(self.DIFFICULTY_LEVELS.items()):
            if params:
                height, width, mines = params
                text = f"{diff} ({width}x{height} board, {mines} mines)"
            else:
                text = diff
            self.difficulty_buttons[diff] = self.create_button(
                text,
                lambda d=diff: self.difficulty_button_click(d),
                bg=colors[i]
            )
        
        self.back_button = self.create_button("Back", self.back_button_click, font_size=18, width_factor=0.01, height_factor=0.001)
        self.try_again_button = self.create_button("Try again", self.try_again_button_click)
        
        # self.lost_title_label = tk.Label(self.window, text="You lost!", font=self.opening_title_font)
        # self.won_title_label = tk.Label(self.window, text="You won!", font=self.opening_title_font)

        self.show_main_menu()

    def create_button(self, text, command, bg='#ffffff', fg='#000000', font_size=24, width_factor=0.02, height_factor=0.002):
        return tk.Button(
            self.window,
            text=text,
            font=("Arial", font_size),
            width=int(self.width * width_factor),
            height=int(self.height * height_factor),
            command=command,
            bg=bg,
            fg=fg
        )

    def show_main_menu(self):
        self.opening_title_label.pack()
        self.play_button.pack(pady=60)
        self.statistics_button.pack(pady=60)
        self.quit_button.pack(pady=60)

    def hide_main_menu(self):
        self.opening_title_label.pack_forget()
        self.play_button.pack_forget()
        self.statistics_button.pack_forget()
        self.quit_button.pack_forget()

    def show_difficulty_menu(self):
        self.choose_diff_label.pack()
        for button in self.difficulty_buttons.values():
            button.pack(pady=40)
        self.back_button.pack(anchor="sw")

    def hide_difficulty_menu(self):
        self.choose_diff_label.pack_forget()
        for button in self.difficulty_buttons.values():
            button.pack_forget()
        self.back_button.pack_forget()

    def play_button_click(self):
        self.hide_main_menu()
        self.show_difficulty_menu()

    def statistics_button_click(self):
        self.hide_main_menu()
        # TODO: add back and reset buttons
        self.statistics()

    def reset_button_click(self):
        self.reset_progress()  # Implement statistics functionality

    def back_button_click(self):
        self.hide_difficulty_menu()
        self.show_main_menu()

    def difficulty_button_click(self, difficulty):
        self.hide_difficulty_menu()
        if difficulty == "Custom":
            self.setup_custom_game()
        else:
            height, width, mines = self.DIFFICULTY_LEVELS[difficulty]
            self.init_game(height, width, mines, difficulty)

    def setup_custom_game(self):
        width = simpledialog.askinteger("Custom Game", "Enter board width (5-50):", minvalue=5, maxvalue=50)
        if width is None:
            self.show_difficulty_menu()
            return

        height = simpledialog.askinteger("Custom Game", "Enter board height (5-50):", minvalue=5, maxvalue=50)
        if height is None:
            self.show_difficulty_menu()
            return

        max_mines = (width * height) - 1
        mines = simpledialog.askinteger("Custom Game", f"Enter number of mines (1-{max_mines}):", minvalue=1, maxvalue=max_mines)
        if mines is None:
            self.show_difficulty_menu()
            return

        self.init_game(height, width, mines, "Custom")

    def try_again_button_click(self):
        self.lost_title_label.pack_forget()
        self.won_title_label.pack_forget()
        self.try_again_button.pack_forget()
        self.show_difficulty_menu()

    def quit_program(self):
        self.window.destroy()

    def init_game(self, height, width, number_of_mines, difficulty):
        self.state = GameState()
        self.game_status = Constants.GAME_STATUS["In progress"]
        self.state.height = height
        self.state.width = width
        self.state.difficulty = difficulty
        self.state.mine_numbers = number_of_mines
        self.state.field = [[Constants.GAME_ENTRY["EMPTY"] for _ in range(width)] for _ in range(height)]
        self.state.result = [[Constants.GAME_ENTRY["EMPTY"] for _ in range(width)] for _ in range(height)]
        self.state.available_tiles = [(x, y) for x in range(width) for y in range(height)]
        
        self.place_mines()
        self.place_numbers()
        self.hide_difficulty_menu()
        self.setup_game_window()

    def place_mines(self):
        mined_tiles = random.sample(self.state.available_tiles, self.state.mine_numbers)
        for x, y in mined_tiles:
            self.state.available_mines.append((y, x))
            self.state.result[y][x] = 'x'
            self.state.available_tiles.remove((x, y))

    def place_numbers(self):
        for i in range(self.state.height):
            for j in range(self.state.width):
                if self.state.result[i][j] == "x":
                    continue
                tile_mine_count = sum(
                    1 for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                    if 0 <= i + dx < self.state.height and 0 <= j + dy < self.state.width
                    and self.state.result[i + dx][j + dy] == "x"
                )
                self.state.result[i][j] = str(tile_mine_count)

    def setup_game_window(self):
        sweeperlib.load_sprites('./sprites')
        sweeperlib.create_window(
            Constants.GAME_CONFIG["SIZE_OF_TILE"] * self.state.width, 
            Constants.GAME_CONFIG["SIZE_OF_TILE"] * self.state.height + Constants.GAME_CONFIG["HEIGHT_OF_BOARD"]
        )
        sweeperlib.set_draw_handler(self.draw_field)
        sweeperlib.set_mouse_handler(self.open_tile)
        self.state.start_time = int(time.time())
        sweeperlib.start()

    def draw_field(self):
        sweeperlib.clear_window()
        height = Constants.GAME_CONFIG["SIZE_OF_TILE"] * self.state.height
        sweeperlib.draw_background()
        sweeperlib.begin_sprite_draw()
        for i, row in enumerate(self.state.field):
            for j, key in enumerate(row):
                sweeperlib.prepare_sprite(key, j * 40, (self.state.height - i - 1) * 40)
        sweeperlib.draw_sprites()
        current_time = int(time.time()) if self.game_status == Constants.GAME_STATUS["In progress"] else self.state.end_time
        sweeperlib.draw_text("Time: " + self.format_time(current_time - self.state.start_time),
                             Constants.GAME_CONFIG["SIZE_OF_TILE"], height, font="Arial",size=30)

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def open_tile(self, x, y, button, mods):
        if self.state.start_time == -1:
            self.state.start_time = time.time()

        x_coord = self.state.height - 1 - y // 40
        y_coord = x // 40

        if button == sweeperlib.MOUSE_LEFT:
            self.handle_left_click(x_coord, y_coord)
        elif button == sweeperlib.MOUSE_RIGHT:
            self.handle_right_click(x_coord, y_coord)

        if len(self.state.available_tiles) == 0:
            self.handle_win()

        sweeperlib.set_draw_handler(self.draw_field)

    def handle_left_click(self, x, y):
        if self.state.field[x][y] != " ":
            return
        if self.state.result[x][y] == "x":
            self.handle_loss()
        elif int(self.state.result[x][y]) > 0:
            self.state.field[x][y] = self.state.result[x][y]
            self.state.available_tiles.remove((y, x))
        else:
            self.floodfill(x, y)

    def handle_right_click(self, x, y):
        if self.state.field[x][y] not in [" ", "f"]:
            return
        self.state.field[x][y] = "f" if self.state.field[x][y] == " " else " "

    def handle_loss(self):
        # self.draw_field()  # Update the display to show all flags
        self.state.end_time = int(time.time())
        for mine_x, mine_y in self.state.available_mines:
            self.state.field[mine_x][mine_y] = "x"
        messagebox.showinfo("Game over!", "You lost!")
        self.update_results_file()
        self.handle_game_window_close()
        

    def handle_win(self):
        # self.draw_field()  # Update the display to show all flags
        self.state.end_time = int(time.time())
        for mine_x, mine_y in self.state.available_mines:
            self.state.field[mine_x][mine_y] = "x"
        messagebox.showinfo("Win!", "You won!")
        self.update_results_file()
        self.handle_game_window_close()

    def handle_game_window_close(self):
        sweeperlib.close()
        self.show_difficulty_menu()


    def floodfill(self, x, y):
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if (y, x) not in self.state.available_tiles:
                continue
            self.state.field[x][y] = self.state.result[x][y]
            self.state.available_tiles.remove((y, x))
            if self.state.result[x][y] == '0':
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < self.state.height and 0 <= new_y < self.state.width:
                            stack.append((new_x, new_y))

    def statistics(self):
        with open("game_results.json", "r") as f:
            data = json.load(f)
        if data != None:
            game_list = data["games"]

            total_time_easy = 0
            games_played_easy = 0
            games_won_easy = 0
            fastest_time_easy = 86400

            total_time_medium = 0
            games_played_medium = 0
            games_won_medium = 0
            fastest_time_medium = 86400

            total_time_hard = 0
            games_played_hard = 0
            games_won_hard = 0
            fastest_time_hard = 86400

            for game in game_list:
                if game['difficulty'] == 'Easy':
                    total_time_easy += int(game['time'])
                    games_played_easy += 1
                    if game['status'] == 'won':
                        games_won_easy += 1

                elif game['difficulty'] == 'Medium':
                    total_time_medium += int(game['time'])
                    games_played_medium += 1
                    if game['status'] == 'won':
                        games_won_medium += 1

                elif game['difficulty'] == 'Hard':
                    total_time_hard += int(game['time'])
                    games_played_hard += 1
                    if game['status'] == 'won':
                        games_won_hard += 1

            for game in game_list:
                if games_played_easy == 0:
                    fastest_time_easy = 0
                else:
                    if fastest_time_easy >= game['time']:
                        fastest_time_easy = game['time']
                
                if games_played_medium == 0:
                    fastest_time_medium = 0
                else:
                    if fastest_time_medium >= game['time']:
                        fastest_time_medium = game['time']

                if games_played_hard == 0:
                    fastest_time_hard = 0
                else:
                    if fastest_time_hard >= game['time']:
                        fastest_time_hard = game['time']


            lst = [("", "Easy", "Medium", "Hard"),
                ("Games played", games_played_easy, games_played_medium, games_played_hard),
                ("Games won", games_won_easy, games_won_medium, games_played_hard),
                ("Fastest time", self.format_time(fastest_time_easy), self.format_time(fastest_time_medium), self.format_time(fastest_time_hard)),
                ("Total time", self.format_time(total_time_easy), self.format_time(total_time_medium), self.format_time(total_time_hard))
                ]
            
            t = Table(self.window, lst)
        

    def update_results_file(self):
        results_file = "game_results.json"
        result = "lost"
        if len(self.state.available_tiles) == 0:
            result = "won"
        difficulty_level = self.state.difficulty
        total_time = self.state.end_time - self.state.start_time
        try:
            with open(results_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        
        if "games" not in data:
            data["games"] = []
    
        data["games"].append({"status": result, "difficulty": difficulty_level, "time": total_time})
        
        with open(results_file, "w") as f:
            json.dump(data, f, indent = 4)

    def reset_progress(self):
        results_file = "game_results.json"
        with open(results_file, "w") as f:
            json.dump({}, f, indent = 4)


if __name__ == "__main__":
    game = MinesweeperGame()
    game.window.mainloop()