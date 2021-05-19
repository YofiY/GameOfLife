import numpy as np
import tkinter as tk

class Game:
    def __init__(self):
        self.ticks = 0
        self.state = 0           # pause=0, play=1
        self.sleep_time = 200   # sleep interval in ms

        self.grid_size = (25,40)

        self.values = np.zeros(self.grid_size,dtype=np.uint8) # matrix of values (1 or 0)
        self.neighbours = np.zeros(self.grid_size,dtype=np.uint8) # neighbours count of each cell
        self.board = np.zeros(self.grid_size,dtype=object) # corresponding board object

        self.screen_size_in_px = 1000 

    def main(self):
        self.GUI()
        self.root.mainloop()

    def GUI(self):
        self.root = tk.Tk()
        self.root.title("Game of Life") 
        self.canvas = tk.Canvas(self.root, width=self.screen_size_in_px, height=self.screen_size_in_px, bg="black")
        self.options = tk.Canvas(self.root, width=200, height=50)

        self.play_btn = tk.Button(self.options, command=self.set_state, text="Play/Pause")
        self.speed_up_btn = tk.Button(self.options, command=self.speed_up, text="Speed Up")
        self.speed_down_btn = tk.Button(self.options, command=self.speed_down, text="Speed Down")
        self.reset_btn = tk.Button(self.options, command=self.reset, text="Reset")

        self.canvas.pack()
        self.options.pack()

        self.play_btn.pack()
        self.speed_up_btn.pack()
        self.speed_down_btn.pack()
        self.reset_btn.pack()

        self.draw()

    def tick(self, n=1):
        self.ticks += n
        self.update()
        print(self.ticks)
        if self.state == 1:
            self.root.after(self.sleep_time, self.tick)

    def set_state(self):
        if self.state == 0:
            self.state =1
            self.tick()
            print('PLAY')
        else:
            self.state = 0
            print('PAUSE')

    def speed_up(self):
        if self.sleep_time > 100: 
            self.sleep_time -= 100

    def speed_down(self):
        if self.sleep_time < 1000: 
            self.sleep_time += 100

    def reset(self):
        self.__init__()
        self.draw()

    def click(self, event):
        info = event.widget.grid_info()
        print(info['row'],info['column'],info['in'])
        print(self.values[info['row']][info['column']])

        if self.values[info['row']][info['column']] == 0:
            self.values[info['row']][info['column']] = 1
            event.widget.config(bg='white')

            self.update_neighbours(False, info['row'], info['column'])
        else:
            self.values[info['row']][info['column']] = 0
            event.widget.config(bg='black')

            self.update_neighbours(True, info['row'], info['column'])

        print('alive neighbours',self.neighbours[info['row']][info['column']])

    def draw(self):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if self.board[row][col] == 0: #if frame doesnt exist, create
                    if not self.values[row][col]:
                        self.board[row][col] = tk.Button(self.canvas, bg='black', bd=0, width = 2, height = 1)
                    else:
                        self.board[row][col] = tk.Button(self.canvas, bg='white', bd=0, width = 2, height = 1)

                    self.board[row][col].grid( row=row, column=col)
                    self.board[row][col].bind('<Button-1>', self.click)
                else:   #else update
                    if not self.values[row][col]:
                        self.board[row][col].config(bg='black')
                    else:
                        self.board[row][col].config(bg='white')

    def update_neighbours(self, died, row, col):
        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:  #if not both are 0
                    try:
                        if died:
                            self.neighbours[row+i][col+j] -= 1
                        else:
                            self.neighbours[row+i][col+j] += 1
                    except: #out of range index error if cell is on edge
                        pass

    def update(self):
        elements = np.nonzero(self.neighbours)
        to_update = []
        for row in elements[0]:
            for col in elements[1]:
                if self.values[row][col] == 0 and self.neighbours[row][col] == 3:
                    print(row,col,'born')
                    self.values[row][col] = 1
                    to_update.append([False,row,col])
                        
                elif self.values[row][col] == 1 and self.neighbours[row][col] != 3 and self.neighbours[row][col] != 2:
                    print(row,col,'died')
                    self.values[row][col] = 0
                    to_update.append([True,row,col])
        
        for el in to_update:    # update neighbours only on at the end
            self.update_neighbours(el[0],el[1],el[2])
        self.draw()  
           

if __name__ == "__main__":
    Game().main()