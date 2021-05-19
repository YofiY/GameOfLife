import numpy as np
import tkinter as tk

class Game:
    def __init__(self):
        self.ticks = 0
        self.state = 0      # pause=0, play=1
        self.zoom = 1       # the zoom scale, higher highest is 1
        self.offset = [500,500]  # (x,y) offset in px
        self.values = [[0]*1000]*1000#np.zeros((1000,1000),dtype=np.uint8) # matrix of values (1 or 0)
        self.neighbours = np.zeros((1000,1000),dtype=np.uint8) # neighbours count of each cell
        self.board = np.zeros((1000,1000),dtype=object) # corresponding board object

        self.zoom = 1 #zoom state: 1 = 100%

    def main(self):
        self.GUI()
        self.binders()
        self.root.mainloop()

    def binders(self):
        self.root.bind('<B1-Motion>', self.drag) #drag
        self.root.bind('<Key>', self.keyboard_event_listener)
        self.root.bind('<space>', self.setState)

    def setState(self, event):
        if self.state == 0:
            self.state =1
            self.tick()
            print('PLAY')
        else:
            self.state = 0
            print('PAUSE')

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


    def click(self, event):
        info = event.widget.grid_info()
        print(info['row'],info['column'],info['in'])
        print(self.values[info['row']][info['column']])

        if self.values[info['row']][info['column']] == 0:
            self.values[info['row']][info['column']] = 1
            event.widget.config(bg='white')

            #self.update_neighbours(False, info['row'], info['column'])
        else:
            self.values[info['row']][info['column']] = 0
            event.widget.config(bg='black')

            #self.update_neighbours(True, info['row'], info['column'])

        #print('alive neighbours',self.neighbours[info['row']][info['column']])

    def draw(self):
        chunk_canvas = tk.Frame(self.canvas, width=self.size_in_px, height=self.size_in_px, bg="black")
        #chunk_canvas.grid( row=chunk[0], column=chunk[1])
        #print(chunk_canvas.grid_info())
        chunk_canvas.pack()
        for row in range(16):
            for col in range(16):
                if not self.values[row+self.offset[0]][col+self.offset[1]]:
                    self.board[row+self.offset[0]][col+self.offset[1]] = tk.Frame(chunk_canvas, bg='black', bd=0, width=(self.size_in_px/16), height=(self.size_in_px/16))
                else:
                    self.board[row+self.offset[0]][col+self.offset[1]] = tk.Frame(chunk_canvas, bg='white', bd=0, width=(self.size_in_px/16), height=(self.size_in_px/16))

                self.board[row+self.offset[0]][col+self.offset[1]].grid( row=row+self.offset[0], column=col+self.offset[1])
                self.board[row+self.offset[0]][col+self.offset[1]].bind('<Button-1>', self.click)

    def update_neighbours(self, died, row, col):
        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:  #if not both are 0
                    if died:
                        self.neighbours[row+i][col+j] -= 1
                    else:
                        self.neighbours[row+i][col+j] += 1

    def update(self):
        for row in range(1000):
            for col in range(1000):
                pass
        self.draw()


    def GUI(self):
        self.root = tk.Tk()
        self.size_in_px = 640
        self.canvas = tk.Canvas(self.root, width=self.size_in_px, height=self.size_in_px, bg="black")
        self.canvas.pack()
        self.draw()

    def tick(self, n=1):
        self.ticks += n
        self.update()
        print(self.ticks)
        if self.state == 1:
            self.root.after(1000, self.tick)

#https://stackoverflow.com/questions/26988204/using-2d-array-to-create-clickable-tkinter-canvas

if __name__ == "__main__":
    Game().main()
