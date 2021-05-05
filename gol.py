import numpy as np
import tkinter as tk

class Game:
    def __init__(self):
        self.ticks = 0
        self.state = 0 #pause=0, play=1
        self.loaded_chunks = {
        #(x,y) : array(16x16)
        (0,0) : [np.zeros((16,16)), np.zeros((16,16)] # matrix base coordinate: list[E, S] where E is the state matrix and S the number of alive neighbours
        }

        self.zoom = 1 #zoom state: 1 = 100%

    def main(self):
        self.GUI()
        self.binders()
        self.root.mainloop()

    def binders(self):
        self.root.bind('<B1-Motion>', self.click) #drag
        self.root.bind('<Key>', self.keyboard_event_listener)

    def GUI(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=640, height=640, bg="black")
        self.canvas.pack()

    def update_matrices(E,S):
        pass

    def tick(self, n=1):
        self.ticks += n

    def motion(self, event):
        print("Mouse position: (%s %s)" % (event.x, event.y))
        return

    def click(self, event):
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

class Grid:
    def __init__(self):

        self.chunk_size = 16    #16x16 block chunks


if __name__ == "__main__":
    Game().main()
