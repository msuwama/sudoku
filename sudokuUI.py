# Module sudokuUI.py
# UI class for the sudoku puzzle app
import tkinter as tk
import tkinter.messagebox
from sudoku import Game, NORMAL, CENTRE, TOP

bigfont = ("Helvetica", 28)
smallfont = ("Helvetica", 12)


class SudokuUI(tk.Frame):
    def __init__(self, parent, size, positions):
        self.board = Game(positions)
        self.board_vars = {}
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Sudoku")
        self.pack(fill=tk.BOTH, padx=50, pady=50)
        self.__draw_grid(size)
        self.cursor = None
        self.__key_bind()
        self.focus_set()
        self.__draw_buttons()

    def __draw_grid(self, size):
        self.grid_canvas = tk.Canvas(self)
        self.grid_canvas.pack(anchor="center", side=tk.LEFT)

        # set up the grid. Even i's are the lines and odd i's are the cells
        for i in range(19):
            # make the line thicker for the border of 3x3
            if i % 6 == 0:
                w = 2
            elif i % 2 == 0:
                w = 1
            else:
                w = size
            self.grid_canvas.grid_rowconfigure(i, minsize=w)
            self.grid_canvas.grid_columnconfigure(i, minsize=w)
        # Construct the sudoku cells
        self.cells = {}
        for i in range(9):
            for j in range(9):
                if (i, j) in self.board.initial_cells:
                    e = tk.Label(self.grid_canvas, bg="white", cursor="hand2",
                                 text=str(self.board.initial_board[(i, j)][1]), font=bigfont)
                else:
                    var = tk.StringVar()
                    self.board_vars[(i, j)] = var
                    e = tk.Label(self.grid_canvas, textvariable=var, fg="navy", bg="white", cursor="hand2", font=bigfont)
                e.bind("<Button-1>", self.__cell_clicked)
                e.grid(row=2 * i + 1, column=2 * j + 1, sticky="nesw")
                e.config(wraplength=50)
                self.cells[(i, j)] = e
        # Draw the grid lines
        for i in range(10):
            tk.Frame(self.grid_canvas, bg='black').grid(
                row=2 * i, column=0, columnspan=19, sticky="news")
            tk.Frame(self.grid_canvas, bg='black').grid(
                column=2 * i, row=0, rowspan=19, sticky="news")

    def __draw_buttons(self):
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.LEFT, padx=20)
        self.inputType = tk.StringVar(self.button_frame, NORMAL)
        tk.Radiobutton(self.button_frame, text="Normal(n)", variable=self.inputType, value=NORMAL).pack(anchor=tk.W)
        tk.Radiobutton(self.button_frame, text="Centre(c)", variable=self.inputType, value=CENTRE).pack(anchor=tk.W)
        tk.Radiobutton(self.button_frame, text="Top(t)", variable=self.inputType, value=TOP).pack(anchor=tk.W)
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.__clear)
        self.clear_button.pack(fill=tk.BOTH, side=tk.LEFT)
        self.check_button = tk.Button(self.button_frame, text="Check", command=self.__check)
        self.check_button.pack(fill=tk.BOTH, side=tk.RIGHT)

    def __cell_clicked(self, event):
        self.__move_cursor(event.widget)

    def __move_cursor(self, new):
        if self.cursor:
            self.cursor["relief"] = "flat"
        self.cursor = new
        new["relief"] = "solid"

    def __key_bind(self):
        self.bind('<Left>', lambda event: self.__movement("left"))
        self.bind('<Right>', lambda event: self.__movement("right"))
        self.bind('<Up>', lambda event: self.__movement("up"))
        self.bind('<Down>', lambda event: self.__movement("down"))
        self.bind('<n>', lambda event: self.__change_input_type(NORMAL))
        self.bind('<c>', lambda event: self.__change_input_type(CENTRE))
        self.bind('<t>', lambda event: self.__change_input_type(TOP))
        self.bind('<Key>', self.__key_pressed)

    def __movement(self, direction):
        if self.cursor:
            i, j = self.__cell_cursor()
            if direction == "left" and  j != 0:  # check if we can go left
                self.__move_cursor(self.cells[(i, j - 1)])
            elif direction == "right" and j != 8:  # check if we can go right
                self.__move_cursor(self.cells[(i, j + 1)])
            elif direction == "up" and i != 0:  # check if we can go up
                self.__move_cursor(self.cells[(i - 1, j)])
            elif direction == "down" and i != 8:  # check if we can go down
                self.__move_cursor(self.cells[(i + 1, j)])
                
    def __change_input_type(self, input_type):
        self.inputType.set(input_type)

    def __key_pressed(self, event):
        if event.char in list("123456789"):
            self.__update_cell(event.char)

    def __update_cell(self, c):
        if self.cursor:
            coord = self.__cell_cursor()
            int_c = int(c)
            if coord not in self.board.initial_cells:
                if self.inputType.get() == NORMAL:
                    self.board.board[coord] = (NORMAL, int_c)
                elif self.inputType.get() == CENTRE:
                    if self.board.board[coord][0] != CENTRE:
                        self.board.board[coord] = (CENTRE, set([int_c]))
                    else:
                        self.board.board[coord][1].symmetric_difference_update([int_c])
                elif self.inputType.get() == TOP:
                    if self.board.board[coord][0] != TOP:
                        self.board.board[coord] = (TOP, set([int_c]))
                    else:
                        self.board.board[coord][1].symmetric_difference_update([int_c])
                self.__update_cell_UI(coord)

    def __update_cell_UI(self, coord):
        status, val = self.board.board[coord]
        if status == NORMAL:
            self.cells[coord].config(anchor=tk.CENTER, font=bigfont, fg="navy")
            self.board_vars[coord].set(val)
        elif status == CENTRE:
            self.cells[coord].config(anchor=tk.CENTER, font=smallfont, fg="blue")
            self.board_vars[coord].set(" ".join(sorted([str(e) for e in val])))
        elif status == TOP:
            self.cells[coord].config(anchor=tk.N, font=smallfont, fg="blue")
            self.board_vars[coord].set(" ".join(sorted([str(e) for e in val])))
    
    def __cell_cursor(self):
        return self.cursor.grid_info()["row"] // 2, self.cursor.grid_info()["column"] // 2

    def __clear(self):
        self.board.reset_board()
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.board.initial_cells:
                    self.board_vars[(i, j)].set("")

    def __check(self):
        tk.messagebox.showinfo(message=self.board.check_win()[1])
