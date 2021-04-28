import numpy as np
import tkinter as tk

class Game:
    def __init__(self):
        self.ticks = 0
        self.state = 0 #pause=0, play=1

    def main(self):
        self.GUI()
        self.root.mainloop()

    def GUI(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=640, height=640, bg="black")
        self.canvas.pack()

    def tick(self, n=1):
        self.ticks += n

class Grid:
    def __init__(self):
        self.chunk_size = 16    #16x16 block chunks

    def chunk(self):
        pass

if __name__ == "__main__":
    Game().main()
