# Module sudokuUI.py
# UI class for the sudoku puzzle app
import tkinter as tk
import tkinter.messagebox
from sudoku import Game

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
                                 text=str(self.board.initial_board[(i, j)]), font=bigfont)
                else:
                    var = tk.StringVar()
                    self.board_vars[(i, j)] = var
                    e = tk.Label(self.grid_canvas, textvariable=var, fg="blue", bg="white", cursor="hand2",
                                 font=bigfont)
                e.bind("<Button-1>", self.__cell_clicked)
                e.grid(row=2 * i + 1, column=2 * j + 1, sticky="nesw")
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
        self.inputType = tk.StringVar()
        self.inputType.set("normal")
        tk.Radiobutton(self.button_frame, text="Normal", variable=self.inputType, value="normal").pack(anchor=tk.W)
        tk.Radiobutton(self.button_frame, text="Centre", variable=self.inputType, value="centre").pack(anchor=tk.W)
        tk.Radiobutton(self.button_frame, text="Corner", variable=self.inputType, value="corner").pack(anchor=tk.W)
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
        self.bind('<Left>', self.__left)
        self.bind('<Right>', self.__right)
        self.bind('<Up>', self.__up)
        self.bind('<Down>', self.__down)
        self.bind('<Key>', self.__key_pressed)

    def __left(self, event):
        if self.cursor:
            i, j = self.__cell_cursor()
            if j != 0:  # check if we can go left
                self.__move_cursor(self.cells[(i, j - 1)])

    def __right(self, event):
        if self.cursor:
            i, j = self.__cell_cursor()
            if j != 8:  # check if we can go left
                self.__move_cursor(self.cells[(i, j + 1)])

    def __up(self, event):
        if self.cursor:
            i, j = self.__cell_cursor()
            if i != 0:  # check if we can go left
                self.__move_cursor(self.cells[(i - 1, j)])

    def __down(self, event):
        if self.cursor:
            i, j = self.__cell_cursor()
            if i != 8:  # check if we can go left
                self.__move_cursor(self.cells[(i + 1, j)])

    def __key_pressed(self, event):
        if event.char in list("123456789"):
            self.__update_cell(event.char)

    def __update_cell(self, c):
        if self.cursor:
            coord = self.__cell_cursor()
            if coord not in self.board.initial_cells:
                if self.inputType.get() == "normal":
                    self.cells[coord].config(anchor=tk.CENTER, font=bigfont)
                elif self.inputType.get() == "centre":
                    self.cells[coord].config(anchor=tk.CENTER, font=smallfont)
                elif self.inputType.get() == "corner":
                    self.cells[coord].config(anchor=tk.NW, font=smallfont)
                self.board_vars[coord].set(c)
                self.board.board[coord] = int(c)

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
