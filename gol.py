import numpy as np
import tkinter as tk

class Game:
    def __init__(self):
        self.ticks = 0
        self.state = 0      # pause=0, play=1
        self.zoom = 1       # the zoom scale, higher highest is 1
        self.offset = [0,0]  # (x,y) offset in px

    def main(self):
        self.GUI()
        self.root.mainloop()

    def GUI(self):
        self.root = tk.Tk()
        self.size_in_px = 640
        self.canvas = tk.Canvas(self.root, width=self.size_in_px, height=self.size_in_px, bg="black")
        self.canvas.pack()

    def draw(self):
        pass

    def tick(self, n=1):
        self.ticks += n

#https://stackoverflow.com/questions/26988204/using-2d-array-to-create-clickable-tkinter-canvas
class Grid:
    def __init__(self):
        self.chunk_size = 16    #16x16 blocks chunks

    def load_chunk(self):
        self.empty = [[0]*self.chunk_size for _ in range(self.chunk_size)]

    def unload_chunk(self): # if chunk is empty, unload it (delete from memory)
        pass

    def update(self):
        pass

if __name__ == "__main__":
    Game().main()
