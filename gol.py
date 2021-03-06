import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename

class Game:
    def __init__(self):
        self.ticks = 0
        self.state = 0           # pause=0, play=1
        self.sleep_time = 5      # sleep interval in ms

        self.grid_size = (200,200)    #needs to be square

        self.values = np.zeros(self.grid_size,dtype=np.uint8)     # matrix of values (1 or 0)
        self.neighbours = np.zeros(self.grid_size,dtype=np.uint8) # matrix of neighbours count of each cell
        self.cells = np.zeros(self.grid_size,dtype=object)        # matrix of cell objects (tk rectangles)

        self.screen_size_in_px = 1000 

    def main(self):
        self.gui()
        self.binders()
        self.root.mainloop()

    def gui(self):
        self.root = tk.Tk()
        self.root.title("Game of Life")
        self.canvas = tk.Canvas(self.root, width=self.screen_size_in_px, height=self.screen_size_in_px, bg="black")
        self.options = tk.Canvas(self.root, width=200, height=50)

        self.play_btn = tk.Button(self.options, command=self.set_state, text="Play/Pause")
        self.speed_label = tk.Label(self.options, text="Set Speed : ")
        self.speed = tk.Scale(self.options, command=self.set_speed, from_=5, to=1000, orient="horizontal")
        self.open_file_btn = tk.Button(self.options, command=self.open_file, text="Select Pattern (.RLE)")
        self.reset_btn = tk.Button(self.options, command=self.reset, text="Reset")
        self.size = tk.Entry(self.options, bd =5)
        self.set_size_btn = tk.Button(self.options, command=self.set_size, text="Set Grid")

        self.canvas.pack()
        self.options.pack()

        self.play_btn.grid(row=0,column=0)
        self.reset_btn.grid(row=0,column=1)
        self.open_file_btn.grid(row=0,column=2)
        self.speed_label.grid(row=0,column=3)
        self.speed.grid(row=0,column=4)
        self.size.grid(row=0,column=5)
        self.set_size_btn.grid(row=0,column=6)

    def tick(self, n=1):
        if self.state:  #if play
            self.ticks += n
            self.update()
            self.canvas.after(self.sleep_time, self.tick)

    #### Options ####
    def set_state(self):
        self.state = 1 if self.state == 0 else 0
        self.tick()

    def set_speed(self,value):
        self.sleep_time = int(value)

    def set_size(self):
        try:
            value = int(self.size.get())
            self.reset()
            self.grid_size = (value,value)
            self.values = np.zeros(self.grid_size,dtype=np.uint8)     # matrix of values (1 or 0)
            self.neighbours = np.zeros(self.grid_size,dtype=np.uint8) # matrix of neighbours count of each cell
            self.cells = np.zeros(self.grid_size,dtype=object)        # matrix of cell objects (tk rectangles)
        except:
            pass

    def open_file(self):     # browse https://www.conwaylife.com/wiki/Main_Page to download .RLE pattern files
        fn = askopenfilename()
        file = open(fn,"r")
        lines = file.read().split('\n')
        pattern, x, y = '','',''
        for line in lines:
            if line[0] != '#':      # /!\ FILE MUST NOT CONTAIN END LINES (''[0] = error)
                if line[0] == 'x':  # first line
                    args = line.split(',')
                    x = int(args[0].split(' ')[-1])
                    y = int(args[1].split(' ')[-1])
                else:
                    pattern += line
        a = []
        for row in pattern.split('$'):
            n = ''
            r = []
            for char in row:
                if char == 'b':
                    if n == '':
                        n = '1'
                    r += int(n)*[0]
                    n = ''
                elif char =='o':
                    if n == '':
                        n = '1'
                    r += int(n)*[1]
                    n = ''
                elif char =='!':
                    r += (x-len(r))*[0]
                    break
                else:
                    n += char
            a.append(r)

        pattern_values = np.rot90(np.fliplr(np.array(a,dtype=np.uint8)),1) 
        x_offset, y_offset = (self.grid_size[0]-x)//2, (self.grid_size[1]-y)//2
        self.values[x_offset:x_offset+pattern_values.shape[0], y_offset:y_offset+pattern_values.shape[1]] = pattern_values

        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                if self.values[x][y]:
                    self.draw_cell(x, y, 'white')
                    self.update_neighbours(False, x, y)

    def reset(self):
        self.__init__()
        self.canvas.delete("all")

    #### Game ####
    def draw_cell(self, x, y, color):
        if color == 'white':
            self.cells[x][y] = self.canvas.create_rectangle(x*int(self.screen_size_in_px/self.grid_size[0]), y*int(self.screen_size_in_px/self.grid_size[1]), (x+1)*int(self.screen_size_in_px/self.grid_size[0]), (y+1)*int(self.screen_size_in_px/self.grid_size[1]), fill=color, width=0, outline=color)
        else:
            self.canvas.delete(self.cells[x][y])

    def binders(self):
        self.canvas.bind('<B1-Motion>', self.drag) #drag
        self.canvas.bind('<Button-1>', self.click)

    def click(self, event):
        x,y = int((event.x/self.screen_size_in_px)*self.grid_size[0]), int((event.y/self.screen_size_in_px)*self.grid_size[1])

        if self.values[x][y] == 0:
            self.values[x][y] = 1
            self.draw_cell(x, y, 'white')
            self.update_neighbours(False, x, y)
        else:
            self.values[x][y] = 0
            self.draw_cell(x, y, 'black')
            self.update_neighbours(True, x, y)

    def drag(self, event):
        x,y = int((event.x/self.screen_size_in_px)*self.grid_size[0]), int((event.y/self.screen_size_in_px)*self.grid_size[1])
        try:
            if self.values[x][y] == 0: # for drag, only activate cells
                self.values[x][y] = 1
                self.draw_cell(x, y, 'white')
                self.update_neighbours(False, x, y)
        except IndexError:
            pass

    def update_neighbours(self, died, x, y):
        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:  #if not both are 0
                    try:
                        if died:
                            self.neighbours[x+i][y+j] -= 1
                        else:
                            self.neighbours[x+i][y+j] += 1
                    except IndexError: #out of range index error if cell is on edge
                        pass

    def update(self):
        will_born = np.argwhere( (self.values == 0) & (self.neighbours == 3))
        will_die = np.argwhere( (self.values == 1) & (self.neighbours != 3) & (self.neighbours != 2))
        to_update = []

        for x,y in will_born:
            self.values[x][y] = 1 # cell born
            self.draw_cell(x, y, 'white')
            to_update.append([False,x,y])
        for x,y in will_die:
            self.values[x][y] = 0 # cell died
            self.draw_cell(x, y, 'black')
            to_update.append([True,x,y])
        
        for el in to_update:    # update neighbours only on at the end
            self.update_neighbours(el[0],el[1],el[2])
                
if __name__ == "__main__":
    Game().main()