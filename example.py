import tkinter as tk
from sudokuUI import SudokuUI

root = tk.Tk()
#p = [ [0,i,i+1] for i in range(9) ] + [ [1,(i+3)% 9, i + 1] for i in range(9)] + [ [2,(i+6) % 9, i+1] for i in range(9)] + [[3,(i+1)%9,i+1] for i in range(9)] + [[4,(i+4)%9,i+1] for i in range(9)] + [[5, (i+7)% 9, i + 1] for i in range(9)]  + [[6,(i+2)%9,i+1] for i in range(9)] + [[7,(i+5)%9,i+1] for i in range(9)] + [[8, (i+8)% 9, i + 1] for i in range(9)]
p = [ [0,i,i+1] for i in range(9) ] + [ [1,(i+3)% 9, i + 1] for i in range(9)] + [ [2,(i+6) % 9, i+1] for i in range(9)] + [[3,(i+1)%9,i+1] for i in range(9)] + [[4,(i+4)%9,i+1] for i in range(9)] + [[5, (i+7)% 9, i + 1] for i in range(9)]  + [[6,(i+2)%9,i+1] for i in range(9)] + [[7,(i+5)%9,i+1] for i in range(9)]
s = SudokuUI(root, 60, p)
root.geometry("800x800")
root.mainloop()