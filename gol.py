import numpy as np
import tkinter as tk

class Game:
    def __init__(self):
        self.ticks = 0
        self.state = 0      # pause=0, play=1
        self.zoom = 1       # the zoom scale, higher highest is 1
        self.offset = [0,0]  # (x,y) offset in px
        self.loaded_chunks = {
        #(x,y) : array(16x16)
        (0,0) : np.zeros((16,16)) # matrix base coordinate: list[E, S] where E is the state matrix and S the number of alive neighbours
        }
        self.zoom = 1 #zoom state: 1 = 100%

    def main(self):
        self.GUI()
        self.binders()
        self.root.mainloop()

    def binders(self):
        self.root.bind('<B1-Motion>', self.drag) #drag
        self.root.bind('<Key>', self.keyboard_event_listener)
        self.root.bind('<Button-1>', self.click)

    def click(self):
        return

    def drag(self, event):
        print('clicked: {}'.format((event.x, event.y)))
        return

    def keyboard_event_listener(self, event):
        if event.keycode == 86 and self.zoom < 1: #86 = + keycode
            self.zoom = round(1.25 * self.zoom, 4)
            print('zoom: {}'.format(self.zoom))

        elif event.keycode == 82: #82 = - keycode
            self.zoom = round(0.8 * self.zoom, 4)
            print('dezoom: {}'.format(self.zoom))
        return

    def GUI(self):
        self.root = tk.Tk()
        self.size_in_px = 640
        self.canvas = tk.Canvas(self.root, width=self.size_in_px, height=self.size_in_px, bg="black")
        self.canvas.pack()

    def draw(self):
        for chunk in loaded_chunks:
            print(chunk)

    def update_matrices(E,S):
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

    def motion(self, event):
        print("Mouse position: (%s %s)" % (event.x, event.y))
        return

if __name__ == "__main__":
    Game().main()
