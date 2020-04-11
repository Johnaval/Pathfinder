from tkinter import *
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
        self.value = 0
        self.color = 'white'
        self.neighbors = []
        self.previous = 0

    def add_neighbors(self, grid):
        #neighbors = [[-1,0], [0,-1], [0,1], [1,0]]
        neighbors = [[-1,-1], [-1,0], [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1]]
        for neighbor in neighbors:
            if self.i+neighbor[0] >= 0 and self.i+neighbor[0] < len(grid[0]) and self.j+neighbor[1] >= 0 and self.j+neighbor[1] < len(grid) and (self.i+neighbor[0] != game.start.i or self.j+neighbor[1] != game.start.j):
                self.neighbors.append(grid[self.i+neighbor[0]][self.j+neighbor[1]])

    def set_color(self):
        if self.value == 0:
            color = 'white'
        elif self.value == 1:
            color = 'black'
        elif self.value == 2:
            color = 'pink'
        elif self.value == 3:
            color = 'red'
        elif self.value == 4:
            color = 'magenta'
        elif self.value == 5:
            color = 'blue'
        self.color = color
    
    def get_color(self):
        return self.color

    def set_value(self, value):
        self.value = value
        self.set_color()

    def get_value(self):
        return self.value

class Game:
    def __init__(self):
        self.grid = [[Spot(i,j) for j in range(width//rect_side)] for i in range(height//rect_side)]
        self.openSet = []
        self.closedSet = []

    def set_start(self, i, j):
        self.start = self.grid[i][j]
        self.openSet.append(self.start)

    def set_end(self, i, j):
        self.end = self.grid[i][j]
    
    def get_color(self, i, j):
        return self.grid[i][j].get_color()

    def set_value(self, i, j, value):
        self.grid[i][j].set_value(value)

    def get_value(self, i, j):
        return self.grid[i][j].get_value()

class GUI:
    def __init__(self):
        self.points = []

        self.root = Tk()
        self.root.title("Pathfinder")
        self.root.resizable(FALSE,FALSE)

        frame = Frame(self.root)
        frame.grid(row = 0, column = 0)
        self.check_var = IntVar()
        c = Checkbutton(frame, text="I want to visualize", variable=self.check_var)
        c.grid(row=0, column=0, padx=5, pady=5)
        button = Button(frame, command = self.Run, text = "Run")
        button.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.canvas = Canvas(self.root, bg = 'white', width = width, height = height, bd = 2, relief = RIDGE)
        self.canvas.grid(row=1, column=0)
        
        self.draw_game()

        self.mouse_clicked = 2
        self.canvas.bind("<Motion>", self.mouse_movement)
        self.canvas.bind('<Button 1>', self.mouse_click)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_release)

        self.root.mainloop()

    def draw_game(self):
        self.canvas.delete(ALL)
        increment = 5
        for i in range(width//rect_side):
            for j in range(height//rect_side):
                x1 = increment + i * rect_side
                y1 = increment + j * rect_side
                x2 = x1 + rect_side
                y2 = y1 + rect_side
                color = game.get_color(i,j)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tag = (i,j))

    def change_rect_color(self, event, value, color):
        item = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)[0]
        tag = self.canvas.gettags(item)
        i,j = int(tag[0]), int(tag[1])
        if game.get_value(i,j) == 0:
            game.set_value(i,j,value)
            self.canvas.itemconfig(item, fill=color)
            self.canvas.update()
            
    def mouse_movement(self, event):
        if self.mouse_clicked == True:
            self.change_rect_color(event, 1, 'black')
    
    def mouse_click(self, event):
        if self.mouse_clicked == 2:
            item = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)[0]
            tag = self.canvas.gettags(item)
            i,j = int(tag[0]), int(tag[1])
            game.set_start(i,j)
            self.points.append([i,j])
            self.change_rect_color(event, 2, 'pink')
        elif self.mouse_clicked == 3:
            item = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)[0]
            tag = self.canvas.gettags(item)
            i,j = int(tag[0]), int(tag[1])
            game.set_end(i,j)
            self.points.append([i,j])
            self.change_rect_color(event, 2, 'pink')
            for i in range(height//rect_side):
                for j in range(width//rect_side):
                    game.grid[i][j].add_neighbors(game.grid)
        else:
            self.change_rect_color(event, 1, 'black')
            self.mouse_clicked = True
    
    def mouse_release(self, event):
        self.mouse_clicked = 3 if self.mouse_clicked == 2 else False

    def heuristic(self, neighbor):
        #d = math.sqrt((neighbor.i - game.end.i)**2 + (neighbor.j - game.end.j)**2)
        d = abs(neighbor.i-game.end.i) + abs(neighbor.j-game.end.j)
        return d

    def Run(self):
        while True:
            if len(game.openSet) > 0:
                lowestIndex = 0
                for i in range(len(game.openSet)):
                    if game.openSet[i].f < game.openSet[lowestIndex].f:
                        lowestIndex = i

                current = game.openSet[lowestIndex]

                if current == game.end:
                    path = []
                    temp = current
                    path.append(temp)
                    while temp.previous != 0:
                        path.append(temp.previous)
                        temp = temp.previous
                        
                    for spot in path:
                        spot.set_value(5)
                    self.draw_game()
                    return False

                game.openSet.remove(current)
                game.closedSet.append(current)

                neighbors = current.neighbors
                for neighbor in neighbors:
                    if neighbor not in game.closedSet and neighbor.get_value() != 1:
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
                            neighbor.set_value(3)

                    self.draw_game()
                    time.sleep(0.0001)
                    self.canvas.update()
            else:
                print('No solution')
                return False

game = Game()
gui = GUI()
