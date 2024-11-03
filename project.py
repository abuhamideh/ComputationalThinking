import tkinter as tk
from tkinter import simpledialog

class Maze:
    def __init__(self, canvas, level):
        self.canvas = canvas
        self.grid_size = 5
        self.cell_size = 60
        self.start = level["start"]
        self.pos = self.start
        self.goal = level["target"]
        self.walls = level["walls"]
        self.create_grid()
        self.draw_walls()
        self.place_player()
        self.place_coin()

    def create_grid(self):
        for i in range(self.grid_size + 1):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.cell_size * self.grid_size)
            self.canvas.create_line(0, i * self.cell_size, self.cell_size * self.grid_size, i * self.cell_size)

    def draw_walls(self):
        for x, y in self.walls:
            self.canvas.create_rectangle(
                x * self.cell_size, y * self.cell_size,
                (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                fill="gray"
            )

    def place_player(self):
        x, y = self.pos
        self.player = self.canvas.create_rectangle(
            x * self.cell_size + 15, y * self.cell_size + 15,
            x * self.cell_size + 45, y * self.cell_size + 45,
            fill="green"
        )

    def place_coin(self):
        x, y = self.goal
        self.coin = self.canvas.create_text(x * self.cell_size + 30, y * self.cell_size + 30, text="💰", font=("Helvetica", 24))

    def move_to(self, new_pos):
        self.pos = new_pos
        x, y = new_pos
        self.canvas.coords(self.player, x * self.cell_size + 15, y * self.cell_size + 15, x * self.cell_size + 45, y * self.cell_size + 45)

    def is_blocked(self, pos):
        return pos in self.walls

    def reset(self):
        self.move_to(self.start)

"""
Defining all global variables here
"""
root = None
maze = None
cmd_queue = []
current_level = 0
loop_mode = False
loop_stack = []
move_btns = {}
cmd_counts = {}
btns_frame = None
exec_btn = None
term_text = None
terminal_lines = []

def main():
    """
    Sets everything up after user clicks the play button, by destroying it and then creating a few global variables for levels and loops and calling setup_level function
    """
    global root, maze, cmd_queue, current_level, loop_mode, loop_stack

    root = tk.Tk()
    root.title("Maze Escape - Welcome")
    root.geometry("700x500")
    welcome_label = tk.Label(root, text="Welcome to the Maze Escape!\nYour goal is to escape the maze through code.", font=("Helvetica", 16))
    welcome_label.pack(pady=20)
    play_button = tk.Button(root, text="Play", command=start_game, font=("Helvetica", 16), bg="lightblue")
    play_button.pack(pady=100)
    credit_label = tk.Label(root, text="Made by: Ali Abu Hamideh", font=("Helvetica", 10))
    credit_label.pack(pady=10)
    note_label = tk.Label(root, text="Note: Play on light mode for best appearance!", font=("Helvetica", 8))
    note_label.pack()

    root.mainloop()

def start_game():
    """
    Called after clicking the play button to start the game. Sets up everything related to the level.
    """
    global maze, cmd_queue, current_level, loop_mode, loop_stack

    root.title("Maze Escape")
    cmd_queue = []
    current_level = 0
    loop_mode = False
    loop_stack = []

    # This deletes the play button screen and sets up the game level
    for widget in root.winfo_children():
        widget.destroy()
    setup_level(current_level)


def setup_level(level_idx):
    """
    This function sets up the level by initialising everything through the frames - for the maze, the buttons and the terminal and the current level info for user

    :param level_idx: Which level currently on
    :type level_idx: int
    :raise TypeError: If level_idx is not an int
    """

    global maze, cmd_counts, loop_mode, cmd_queue, btns_frame, exec_btn, term_text, lr_frame
    cmd_queue.clear()
    loop_mode = False
    level = levels[level_idx]
    cmd_counts = level.get("command_counts", {}).copy()

    # Deletes the previous widgets because there was an issue of the buttons duplicating if user was repeating a level after failing - was annoying ngl lol
    for widget in root.winfo_children():
        widget.destroy()

    left_frame = tk.Frame(root)
    right_frame = tk.Frame(root)
    left_frame.pack(side="left", padx=10, pady=10)
    right_frame.pack(side="right", padx=10, pady=10)
    maze_canvas = tk.Canvas(left_frame, bg="white", width=300, height=300)
    maze_canvas.pack()
    maze = Maze(maze_canvas, level)

    level_label = tk.Label(left_frame, text=f"Level {level_idx}: {level['description']}", font=("Helvetica", 14))
    level_label.pack(pady=10)

    btns_frame = tk.Frame(right_frame)
    btns_frame.pack(side="top", anchor="n")
    # This frame is for the Loop and End buttons - so that they can be next to each other - which looks nicer!
    lr_frame = tk.Frame(right_frame)
    lr_frame.pack(side="top", anchor="n")

    create_cmd_buttons()

    exec_btn = tk.Button(right_frame, text="Execute()", command=execute_cmds, font=("Helvetica", 12), bg="LimeGreen")
    exec_btn.pack(pady=10)

    # Execution Terminal Frame - This is last because otherwise the terminal would be above the buttons sadly
    terminal_frame = tk.Frame(right_frame)
    terminal_frame.pack(pady=10)
    term_text = tk.Text(terminal_frame, height=15, width=40, bg="black")
    term_text.pack(side="left", fill="both")
    term_text.configure(font=("Helvetica", 12), fg="white")

levels = [
    # Level 0
    {
        'description': 'Reach the coin!',
        'command_counts': {'up': 3},
        'start': (2, 4),
        'target': (2, 1),
        'walls': [(1, 4), (3, 4), (1, 3), (3, 3), (1, 2), (3, 2), (1, 1), (3, 1)],
    },
    # Level 1
    {
        'description': 'Navigate the maze!',
        'command_counts': {'up': 3, 'right': 5},
        'start': (0, 4),
        'target': (4, 2),
        'walls': [(1, 3), (3, 1)],
    },
    # Level 2
    {
        'description': 'Think outside the box now :)',
        'command_counts': {'up': 1},
        'start': (2, 4),
        'target': (2, 1),
        'walls': [(1, 4), (3, 4), (1, 3), (3, 3), (1, 2), (3, 2), (1, 1), (3, 1)],
        'loops_enabled': True,
    },
    # Level 3
    {
        'description': 'Think carefully about how to use loops here',
        'command_counts': {'up': 4, 'right': 1},
        'start': (0, 4),
        'target': (4, 0),
        'walls': [(2, 2), (2, 3), (2, 1)],
        'loops_enabled': True,
    },
    # Level 4
    {
        'description': 'Loops are your best friend again!',
        'command_counts': {'up': 1, 'right': 1, 'left': 1},
        'start': (4, 4),
        'target': (0, 0),
        'walls': [(2, 3), (2, 2), (2, 1), (1, 1), (3, 3)],
        'loops_enabled': True,
    },
    # Level 5
    {
        'description': 'The ultimate challenge!',
        'command_counts': {'up': 1, 'right': 1, 'down': 1, 'left': 1},
        'start': (3, 1),
        'target': (1, 3),
        'walls': [(1, 2), (2, 2), (3, 2), (2, 1), (2, 3)],
        'loops_enabled': True,
    },
]

def create_cmd_buttons():
    """
    This function sets up the buttons in order to be able to used to create (or re-create if the user is repeating a level after failing) the buttons in level
    """
    global btns_frame, move_btns, cmd_counts, lr_frame
    button_font = ("Helvetica", 12)
    move_btns.clear()
    level = levels[current_level]
    cmd_counts = level.get("command_counts", {}).copy()

    # Clears existing buttons for either the movement buttons or for the lr_frame (i.e which is what i used for the Loop + End button)
    for widget in (*btns_frame.winfo_children(), *lr_frame.winfo_children()):
        widget.destroy()

    for cmd in cmd_counts:
        btn_text = f"Move_Player.{cmd}({cmd_counts[cmd]})"
        btn = tk.Button(btns_frame, text=btn_text, command=lambda c=cmd: add_cmd(c), font=button_font)
        btn.pack(pady=5, anchor="n")
        move_btns[cmd] = btn

    if level.get("loops_enabled"):
        loop_start_btn = tk.Button(lr_frame, text="For x times do:", command=start_loop, font=button_font)
        loop_start_btn.pack(side="left", padx=5)

        loop_end_btn = tk.Button(lr_frame, text="End", command=end_loop, font=button_font)
        loop_end_btn.pack(side="left", padx=5)

def start_loop():
    """
    This function acts to when the user clicks the loop button, this function will be called in which it asks the user how many times they want the loop to be
    """
    global loop_mode
    times = simpledialog.askinteger("Input", "Enter the number of times:")
    if times and times > 0:
        loop_mode = True
        line_num = append_to_terminal(f"For {times} times do:")
        loop_stack.append({'times': times, 'commands': [], 'line_number': line_num})

def end_loop():
    """
    This function acts to when the user clicks the End button - after inputting the loop - to then start popping it and going through it essentially
    """
    global loop_mode
    if loop_mode:
        loop_mode = False
        loop = loop_stack.pop()
        end_line_num = append_to_terminal("End")
        loop["end_line_number"] = end_line_num
        cmd_queue.append({'loop': loop})

def add_cmd(command):
    """
    Once user clicks a movement command button; this is called which adds the command to the queue ready to be executed after the execution button is called

    :param command: The command to append to the queue
    :type command: str
    :raise TypeError: If command is not a str
    """
    if cmd_counts.get(command, 0) > 0:
        cmd_counts[command] -= 1
        if loop_mode:
            loop_stack[-1]["commands"].append(command)
            append_to_terminal(f"    Move_Player.{command}()")
        else:
            line_num = append_to_terminal(f"Move_Player.{command}()")
            cmd_queue.append({'command': command, 'line_number': line_num})
        update_buttons(command)

def execute_cmds():
    """
    Once the execution button is clicked by user this function disabled all buttons so that the loop cant be interrupted; and it calls the function to start executing commands line by line
    """
    disable_buttons()
    execute_next_command(0)

def execute_next_command(index):
    """
    This function takes the index of which command to execute (usually the first one in the command queue)
    and then does so whilst also switching colours from yellow to green in terminal so that it adds to the effect of user seeing which line is doing what
    whilst also timing commands to move the player and recursively calling itself

    :param index: index of the command to execute
    :type index: int
    :raise TypeError: If index is not an int
    """

    if index >= len(cmd_queue):
        return check_completion()
    cmd = cmd_queue[index]
    if "loop" in cmd:
        loop = cmd["loop"]
        loop_times = loop["times"]
        commands = loop["commands"]
        loop_line_num = loop["line_number"]
        highlight_terminal_line(loop_line_num, "yellow")
        def after_loop():
            highlight_terminal_line(loop_line_num, "green")
            highlight_terminal_line(loop["end_line_number"], "green")
            execute_next_command(index + 1)
        execute_loop_commands(commands, loop_times, 0, after_loop)
    else:
        line_num = cmd["line_number"]
        highlight_terminal_line(line_num, "yellow")
        root.after(500, lambda: move_player(maze, cmd["command"]))
        root.after(1000, lambda: highlight_terminal_line(line_num, "green"))
        root.after(1500, lambda: execute_next_command(index + 1))

def execute_loop_commands(commands, loop_times, current_iteration, callback):
    if current_iteration >= loop_times:
        return callback()

    def execute_command_in_loop(idx):
        if idx >= len(commands):
            return execute_loop_commands(commands, loop_times, current_iteration + 1, callback)
        cmd = commands[idx]
        root.after(500, lambda: move_player(maze, cmd))
        root.after(1000, lambda: execute_command_in_loop(idx + 1))
    execute_command_in_loop(0)

def move_player(maze, direction):
    """
    This function takes the command of the user, so as to calculate the logic of doing so; i.e the direction command will be like "up", and this will calculate the logic.
    If there is no wall blocking the intended movement; then the player will move to it

    :param direction: Direction of where the player wishes to move
    :type direction: str
    :raise TypeError: If index is not an int
    """
    x, y = maze.pos
    delta = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
    dx, dy = delta.get(direction, (0, 0))
    new_pos = (x + dx, y + dy)
    if (0 <= new_pos[0] < maze.grid_size and 0 <= new_pos[1] < maze.grid_size and not maze.is_blocked(new_pos)):
        maze.move_to(new_pos)

def check_completion():
    """
    This functions checks that if the user has successfully completed the level then it'll print out a congratulatory message in terminal followed by moving to next level,
     and if not, then a fail message in terminal followed by repeating the current level until they pass
    """
    append_to_terminal("🎉 Level Completed!" if maze.pos == maze.goal else "❌ Level Failed. Try Again!", "gold" if maze.pos == maze.goal else "red")
    root.after(2000, next_level if maze.pos == maze.goal else reset_level)

def next_level():
    """
    This function, after being called by check completion, checks if there are any more levels to complete - and if so, will set it up by calling the function,
    though if there arent anymore levels once user completes them, then it'll print out a congratulatory message
    """
    global current_level
    current_level += 1
    if current_level < len(levels):
        setup_level(current_level)
    else:
        victory_label = tk.Label(root, text="🏆 Congrats!! You completed all levels!", fg="indigo", bg="white", font=("Helvetica", 20))
        victory_label.place(relx=0.5, rely=0.5, anchor="center")

def reset_level():
    """
    This function is called in the check completion function if the user failed the level, and so it'll reset the terminal
    and the level and reinitalise the variables - essentially to start afresh
    """
    global cmd_queue, loop_mode, loop_stack, cmd_counts
    cmd_queue.clear()
    loop_mode = False
    loop_stack = []
    term_text.delete("1.0", tk.END)
    maze.reset()
    level = levels[current_level]
    cmd_counts = level.get("command_counts", {}).copy()
    create_cmd_buttons()
    exec_btn.config(state="normal")

def disable_buttons():
    """
    This function is called in order to disable the buttons from being able to be selected once the code is being executed
    """
    exec_btn.config(state="disabled")
    for widget in (*btns_frame.winfo_children(), *lr_frame.winfo_children()):
        if isinstance(widget, tk.Button):
            widget.config(state="disabled")

def update_buttons(command):
    """
    This function is called after the user clicks a movement button; as they have a finite number of buttons, so this will look at the count and decrement it
    or destory it once it reaches 0

    :param command: current command
    :type command: str
    :raise TypeError: If command is not a str
    """

    if cmd_counts[command] > 0:
        btn_text = f"Move_Player.{command}({cmd_counts[command]})"
        move_btns[command].config(text=btn_text)
    else:
        move_btns[command].destroy()
        del move_btns[command]

def append_to_terminal(text, color="white"):
    """
    This function takes the name of the movement command so that it can print it out on the terminal screen, in white by default, until the code executes

    :param text: The name of the movement command to append to the terminal
    :param color: The colour of the text (by default white until execution)
    :type text: str
    :type color: str
    :raise TypeError: If text or color are not strings
    """

    global terminal_lines
    line_num = term_text.index("end-1c").split(".")[0]
    term_text.insert(tk.END, text + "\n")
    tag_name = f"line{line_num}"
    term_text.tag_add(tag_name, f"{line_num}.0", f"{line_num}.end")
    term_text.tag_configure(tag_name, foreground=color)
    term_text.see(tk.END)
    terminal_lines.append(tag_name)
    return line_num

def highlight_terminal_line(line_num, color):
    """
    This function takes the number of the line being executed and the colour configurations, so that it can change between yellow and green
    after being called by the execute next command function

    :param line_num: The number of the line currently being executed
    :param color: The colour of the text to change into
    :type line_num: int
    :type color: str
    :raise TypeError: If line_num is not int or if color is not str
    """
    tag_name = f"line{line_num}"
    term_text.tag_configure(tag_name, foreground=color)

if __name__ == "__main__":
    main()
