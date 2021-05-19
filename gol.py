import numpy as np
import tkinter as tk

class Game:
    def __init__(self):
        self.ticks = 0
        self.state = 0      # pause=0, play=1
        self.zoom = 1       # the zoom scale, higher highest is 1
        self.offset = [0,0]  # (x,y) offset in px
        self.values = np.zeros((16,16),dtype=np.uint8) # matrix of values (1 or 0)

        self.board = np.zeros((16,16),dtype=object) # corresponding board object

        self.zoom = 1 #zoom state: 1 = 100%

    def main(self):
        self.GUI()
        self.binders()
        self.root.mainloop()

    def binders(self):
        self.root.bind('<B1-Motion>', self.drag) #drag
        self.root.bind('<Key>', self.keyboard_event_listener)

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

    def click(self, event):
        info = event.widget.grid_info()
        print(info['row'],info['column'],info['in'])
        print(self.values[info['row']][info['column']])

        if self.values[info['row']][info['column']] == 0:
            self.values[info['row']][info['column']] = 1
            event.widget.config(bg='white')
        else:
            self.values[info['row']][info['column']] = 0
            event.widget.config(bg='black')

    def draw(self):
        chunk_canvas = tk.Frame(self.canvas, width=self.size_in_px, height=self.size_in_px, bg="black")
        #chunk_canvas.grid( row=chunk[0], column=chunk[1])
        #print(chunk_canvas.grid_info())
        chunk_canvas.pack()
        for row in range(16):
            for col in range(16):
                if not self.values[row][col]:
                    self.board[row][col] = tk.Frame(chunk_canvas, bg='black', bd=0, width=(self.size_in_px/16), height=(self.size_in_px/16))
                else:
                    self.board[row][col] = tk.Frame(chunk_canvas, bg='white', bd=0, width=(self.size_in_px/16), height=(self.size_in_px/16))
                self.board[row][col].grid( row=row, column=col)
                self.board[row][col].bind('<Button-1>', self.click)

    def GUI(self):
        self.root = tk.Tk()
        self.size_in_px = 640
        self.canvas = tk.Canvas(self.root, width=self.size_in_px, height=self.size_in_px, bg="black")
        self.canvas.pack()
        self.draw()

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
