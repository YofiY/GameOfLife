import numpy as np
import tkinter as tk

class Game:
    def __init__(self):
        self.ticks = 0
        self.state = 0      # pause=0, play=1
        self.zoom = 1       # the zoom scale, higher highest is 1
        self.offset = [0,0]  # (x,y) offset in px
        self.loaded_chunks = {(0,0) : np.zeros((16,16)),} # matrix base coordinate: list[E, S] where E is the state matrix and S the number of alive neighbours
        self.zoom = 1 #zoom state: 1 = 100%

    def main(self):
        self.GUI()
        self.binders
        self.gamelogic()
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
        pass

    def gamelogic(self):
        for base in self.loaded_chunks:
            chunk = self.loaded_chunks[base]
            right_base, left_base, bottom_base, top_base = (base[0]+16, base[1]), (base[0]-16, base[1]), (base[0], base[1]-16), (base[0])
            print(chunk)
            print(np.shape(chunk))

            for i in range(16):
                for j in range(16):
 #-------------------------------------
                    if i != 0 and j == 0 :
                      if chunk[i][j] and top_chunk not in loaded_chunks:
                        load_chunk(top_chunk)
                         
                      elif top_chunk in loaded_chunks:
                        S += top_chunk[i][15]
 #-------------------------------------
                if j == 15 and i != 0:
                  if chunk[i][j]:
                    load(bottom_chunk)

                  elif bottom_chunk in loaded_chunks:
                    S += bottom_chunk[i][0]
 #-------------------------------------
                if i == 0 and j != 0:
                  if chunk[i][j]:
                    load(left_chunk)

                  elif left_chunk in loaded_chunks:
                    S += left_chunk[15][j]
 #-------------------------------------
                if i == 15 and j != 0:
                  if chunk[i][j]:
                    load(right_chunk)

                  elif right_chunk in loaded_chunks:
                    S += right_chunk[0][j]
 #-------------------------------------
                if i == 0 and j == 0:
                    pass
 #-------------------------------------
                if i == 15 and j == 15:
                    pass
#--------------------------------------
                if i == 0 and j == 15:
                    pass
 #-------------------------------------
                if i == 15 and j == 0:
                    pass


    def update_matrices(E,S):
        pass

    def tick(self, n=1):
        self.ticks += n

#https://stackoverflow.com/questions/26988204/using-2d-array-to-create-clickable-tkinter-canvas
class Grid:
    def __init__(self):
        self.chunk_size = 16    #16x16 blocks chunks

    def binders(self):
        self.root.bind('<B1-Motion>', self.click) #drag
        self.root.bind('<Key>', self.keyboard_event_listener)

    def load_chunk(self):
        self.empty = [[0]*self.chunk_size for _ in range(self.chunk_size)]

    def unload_chunk(self): # if chunk is empty, unload it (delete from memory)
        pass

    def update_matrices(E,S):
        pass

    def motion(self, event):
        print("Mouse position: (%s %s)" % (event.x, event.y))
        return

if __name__ == "__main__":
    Game().main()
