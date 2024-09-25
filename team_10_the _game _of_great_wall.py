import tkinter as tk
from collections import deque




def is_wall(board, n):
    # Check if the stones are in a straight line either horizontally, vertically, or diagonally
    return any(all(board[i][j] == '0' for j in range(n)) for i in range(n)) or \
           any(all(board[i][j] == '0' for i in range(n)) for j in range(n)) or \
           all(board[i][i] == '0' for i in range(n)) or \
           all(board[i][n - 1 - i] == '0' for i in range(n))

def get_next_moves(board, n):
    # Generate all possible moves for each stone
    moves = []
    for i in range(n):


        for j in range(n):
            if board[i][j] == '0':
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    x, y = i + dx, j + dy
                    if 0 <= x < n and 0 <= y < n and board[x][y] == ' ':
                        moves.append(((i, j), (x, y)))
    print(moves)
    return moves

def bfs(board, n):
    # Use BFS to find the minimum number of moves needed to create a wall
    queue = deque([(board, 0)])
    visited = set()
    visited.add(tuple(''.join(row) for row in board))

    while queue:
        curr_board, moves_count = queue.popleft()

        if is_wall(curr_board, n):
            return moves_count

        for move in get_next_moves(curr_board, n):
            new_board = [row[:] for row in curr_board]
            (x1, y1), (x2, y2) = move
            new_board[x1][y1] = ' '
            new_board[x2][y2] = '0'
            new_board_str = tuple(''.join(row) for row in new_board)

            if new_board_str not in visited:
                queue.append((new_board, moves_count + 1))
                visited.add(new_board_str)

    return -1

def draw_board(canvas, n, board, stone_buttons):
    cell_size =60
    canvas.delete("all")
    canvas.config(width=n * cell_size, height=n * cell_size)
    for i in range(n):
        for j in range(n):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = (j + 1) * cell_size, (i + 1) * cell_size
            if board[i][j] == ' ':
                canvas.create_rectangle(x1, y1, x2, y2, fill="brown", outline="black")
            else:
                canvas.create_rectangle(x1, y1 , x2 , y2 , fill="brown")
                canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="grey")

    for i in range(n):
        for j in range(n):
            stone_buttons[i][j].config(state=tk.NORMAL if board[i][j] == ' ' else tk.DISABLED)


    for i in range(n):
        for j in range(n):
            stone_buttons[i][j].config(state=tk.NORMAL if board[i][j] == ' ' else tk.DISABLED)

def draw_arrow(x1, y1, x2, y2):
    cell_size = 60
    x1_px, y1_px = y1 * cell_size + cell_size // 2, x1 * cell_size + cell_size // 2
    x2_px, y2_px = y2 * cell_size + cell_size // 2, x2 * cell_size + cell_size // 2
    canvas.create_line(y1_px, x1_px, y2_px, x2_px, arrow=tk.LAST, arrowshape=(10, 12, 5), width=2, fill="red")

def animate_moves(canvas, board, moves, delay=1500):
    n = len(board)
    cell_size =60

    def move_stone(move):
        (x1, y1), (x2, y2) = move
        x1_px, y1_px = y1 * cell_size + cell_size // 2, x1 * cell_size + cell_size // 2
        x2_px, y2_px = y2 * cell_size + cell_size // 2, x2 * cell_size + cell_size // 2

        # Draw the arrow from initial position to final position
        draw_arrow(x1, y1, x2, y2)

        # Move the stone along the arrow path
        num_steps = max(abs(x2 - x1), abs(y2 - y1))
        step_x, step_y = (x2 - x1) / num_steps, (y2 - y1) / num_steps

        for step in range(1, num_steps + 1):
            x_step_px, y_step_px = y1_px + step * step_y * cell_size, x1_px + step * step_x * cell_size
            stone_coords = (y_step_px - cell_size // 4, x_step_px - cell_size // 4,
                            y_step_px + cell_size // 4, x_step_px + cell_size // 4)
            canvas.coords(stone, stone_coords)
            canvas.update()
            canvas.after(delay)

        # Update the board and draw the stone at the final position
        board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]
        draw_board(canvas, n, board, stone_buttons)

    stone = None  # Initialize stone as None

    for move in moves:
        if stone:
            canvas.delete(stone)  # Remove the previous stone

        move_stone(move)

        # Create the stone at the final position
        (x1, y1), (x2, y2) = move
        x2_px, y2_px = y2 * cell_size + cell_size // 2, x2 * cell_size + cell_size // 2
        stone = canvas.create_oval(y2_px - cell_size // 4, x2_px - cell_size // 4,
                                   y2_px + cell_size // 4, x2_px + cell_size // 4, fill="black")

    # Draw the final board after all animations are complete
    draw_board(canvas, n, board, stone_buttons)


    if is_wall(board, n):
      result_text.config(state=tk.NORMAL)
      result_text.delete(1.0, tk.END)
      result_text.insert(tk.END, "Required wall is formed!")
      result_text.config(state=tk.DISABLED)


    # Check if there is only one stone on the board and no moves needed
    if len(board) == 1 and (len(moves) == 0 or (len(moves) == 1 and moves[0][0] == moves[0][1])):
        # If there is only one stone and no moves, no animation needed
        return("required wall is formed")

    move_stone(moves)
    
    

        # Schedule the next movement with a delay
     #canvas.after(delay, lambda: move_stone(moves[1:]))

    #move_stone(moves)

def on_stone_click(row, col):
    global board
    board[row][col] = '0' if board[row][col] == ' ' else ' '
    draw_board(canvas, n, board, stone_buttons)

def process_input():
    global n, board, stone_buttons

    min_moves = bfs(board, n)

    if min_moves != -1:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Minimum moves to form the wall: {min_moves}")
        result_text.config(state=tk.DISABLED)

        moves = []
        while min_moves > 0:
            for move in get_next_moves(board, n):
                new_board = [row[:] for row in board]
                (x1, y1), (x2, y2) = move
                new_board[x1][y1] = ' '
                new_board[x2][y2] = '0'
                if bfs(new_board, n) == min_moves - 1:
                    moves.append(move)
                    board = new_board
                    min_moves -= 1
                    break

        animate_moves(canvas, board, moves, delay=1000)

    else:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "No solution!")
        result_text.config(state=tk.DISABLED)

def create_stone_buttons():
    stone_buttons = []
    for i in range(n):
        row_buttons = []
        for j in range(n):
            btn = tk.Button(board_frame, text="", width=2, height=1, command=lambda i=i, j=j: on_stone_click(i, j))
            btn.grid(row=i, column=j)
            row_buttons.append(btn)
        stone_buttons.append(row_buttons)
    return stone_buttons

def main():
    global n, board, canvas, result_text, stone_buttons, board_frame

   
    welcome.destroy()
    start.destroy()
    input_frame = tk.Frame(root)
    input_frame.pack()

    input_label = tk.Label(input_frame, text="Enter board size (n):")
    input_label.pack(side=tk.LEFT)

    size_entry = tk.Entry(input_frame, width=5)
    size_entry.pack(side=tk.LEFT)

    stones_label = tk.Label(input_frame, text="Click on the buttons to place stones:")
    stones_label.pack()

    board_frame = tk.Frame(root)
    board_frame.pack()

    result_text = tk.Text(root, width=40, height=1, state=tk.DISABLED)
    result_text.pack()

    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    def process_input_click():
        global n, board, stone_buttons

        n = int(size_entry.get())
        board = [[' ' for _ in range(n)] for _ in range(n)]

        stone_buttons = create_stone_buttons()
        draw_board(canvas, n, board, stone_buttons)

    process_button = tk.Button(input_frame, text="Enter", command=process_input_click)
    process_button.pack()

    enter_button = tk.Button(root, text="Process Input", command=process_input)
    enter_button.pack()

    

root =tk.Tk()
root.title("The Great Wall Game Solver")
root.configure(bg="light blue") 
welcome=tk.Label(root,text="WELCOME TO THE GAME OF GREAT WALL")
welcome.configure(bg="pink")
welcome.pack()
start=tk.Button(root,text="start game",command=main)
start.pack()
root.mainloop()
