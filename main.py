from tkinter import *
from tkinter import messagebox
import time
import math

width = 500
height = 500
rect_side = 20

class Spot:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = 0
        self.wall = False
        self.item = 0

    def add_neighbors(self, grid):
        #neighbors = [[-1,0], [0,-1], [0,1], [1,0]] #without diagonals
        neighbors = [[-1,-1], [-1,0], [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1]] #with diagonals
        for neighbor in neighbors:
            if self.i+neighbor[0] >= 0 and self.i+neighbor[0] < len(grid[0]) and self.j+neighbor[1] >= 0 and self.j+neighbor[1] < len(grid) and (self.i+neighbor[0] != game.start.i or self.j+neighbor[1] != game.start.j):
                self.neighbors.append(grid[self.i+neighbor[0]][self.j+neighbor[1]])

class Game:
    def __init__(self):
        self.grid = [[Spot(i,j) for j in range(width//rect_side)] for i in range(height//rect_side)]
        self.openSet = []
        self.closedSet = []
        self.path = []

    def define_gui(self, gui):
        self.gui = gui

    def heuristic(self, neighbor):
        #d = math.sqrt((neighbor.i - game.end.i)**2 + (neighbor.j - game.end.j)**2) #Euclidian distance
        d = abs(neighbor.i-game.end.i) + abs(neighbor.j-game.end.j) #Manhattan distance
        return d
    
    def Run(self):
        if gui.start == 0 or gui.end == 0:
            messagebox.showerror('Error', 'First define start and end')
            return False

        self.start = self.grid[self.gui.start[0]][self.gui.start[1]]
        self.openSet.append(self.start)
        self.end = self.grid[self.gui.end[0]][self.gui.end[1]]

        for i in range(height//rect_side):
            for j in range(width//rect_side):
                game.grid[i][j].add_neighbors(game.grid)

        while True:
            if len(game.openSet) > 0:
                lowestIndex = 0
                for i in range(len(game.openSet)):
                    if game.openSet[i].f < game.openSet[lowestIndex].f:
                        lowestIndex = i

                current = game.openSet[lowestIndex]

                if current == game.end:
                    self.path = []
                    temp = current
                    self.path.append(temp)
                    while temp.previous != 0:
                        self.path.append(temp.previous)
                        temp = temp.previous
                        
                    self.gui.update_game()
                    return False

                game.openSet.remove(current)
                game.closedSet.append(current)

                neighbors = current.neighbors
                for neighbor in neighbors:
                    if neighbor not in game.closedSet and neighbor.wall == False:
                        tempG = current.g + 1
                        newPath = False
                        if neighbor in game.openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            game.openSet.append(neighbor)
                        if newPath:
                            neighbor.h = self.heuristic(neighbor)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.previous = current

                    if gui.check_var.get() == 1:
                        self.gui.update_game()
            else:
                self.gui.update_game()
                messagebox.showerror('Error', 'No solution')
                return False

class GUI:
    def __init__(self):
        self.start = 0
        self.end = 0

        self.root = Tk()
        self.root.title("Pathfinder")
        self.root.resizable(FALSE,FALSE)

        frame = Frame(self.root)
        frame.grid(row = 0, column = 0)
        self.check_var = IntVar()
        c = Checkbutton(frame, text="I want to visualize", variable=self.check_var)
        c.grid(row=0, column=0, padx=5, pady=5)
        button = Button(frame, command = game.Run, text = "Run")
        button.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.canvas = Canvas(self.root, bg = 'white', width = width, height = height, bd = 2, relief = RIDGE)
        self.canvas.grid(row=1, column=0)
        
        self.draw_game()

        self.mouse_clicked = 2
        self.canvas.bind("<Motion>", self.mouse_movement)
        self.canvas.bind('<Button 1>', self.mouse_click)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_release)

    def draw_game(self):
        increment = 5
        for i in range(width//rect_side):
            for j in range(height//rect_side):
                x1 = increment + i * rect_side
                y1 = increment + j * rect_side
                x2 = x1 + rect_side
                y2 = y1 + rect_side
                item = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', tag = (i,j))
                game.grid[i][j].item = item

    def update_game(self):
        for spot in game.openSet:
            self.canvas.itemconfig(spot.item, fill='magenta')
            self.canvas.update()

        for spot in game.closedSet:
            self.canvas.itemconfig(spot.item, fill='red')
            self.canvas.update()

        for spot in game.path:
            self.canvas.itemconfig(spot.item, fill='blue')
            self.canvas.update()
            
    def change_rect_color(self, item, color):
        self.canvas.itemconfigure(item, fill=color)
        self.canvas.update()
    
    def mouse_movement(self, event):
        try:
            item = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)[0]
            tag = self.canvas.gettags(item)
            i,j = int(tag[0]), int(tag[1])
        except: pass
        if self.mouse_clicked == True and [i,j] != self.start and [i,j] != self.end:
            self.change_rect_color(item, 'black')
            game.grid[i][j].wall = True
    
    def mouse_click(self, event):
        item = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)[0]
        tag = self.canvas.gettags(item)
        i,j = int(tag[0]), int(tag[1])
        if self.mouse_clicked == 2:
            self.start = [i,j]
            self.change_rect_color(item, 'pink')
        elif self.mouse_clicked == 3:
            self.end = [i,j]
            self.change_rect_color(item, 'pink')
        else:
            if [i,j] != self.start and [i,j] != self.end:
                self.change_rect_color(item, 'black')
                game.grid[i][j].wall = True
                self.mouse_clicked = True
    
    def mouse_release(self, event):
        self.mouse_clicked = 3 if self.mouse_clicked == 2 else False

game = Game()
gui = GUI()
game.define_gui(gui)
gui.root.mainloop()