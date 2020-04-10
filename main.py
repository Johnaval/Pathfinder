from tkinter import *
import time

class GUI:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.rect_side = 20
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

        self.canvas = Canvas(self.root, bg = 'white', width = self.width, height = self.height, bd = 2, relief = RIDGE)
        self.canvas.grid(row=1, column=0)

        self.game = [[0 for j in range(self.width//self.rect_side)] for i in range(self.height//self.rect_side)]
        
        self.draw_game()

        self.mouse_clicked = 2
        self.canvas.bind("<Motion>", self.mouse_movement)
        self.canvas.bind('<Button 1>', self.mouse_click)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_release)

        self.root.mainloop()

    def draw_game(self):
        self.canvas.delete(ALL)
        increment = 5
        for i in range(self.width//self.rect_side):
            for j in range(self.height//self.rect_side):
                x1 = increment + i * self.rect_side
                y1 = increment + j * self.rect_side
                x2 = x1 + self.rect_side
                y2 = y1 + self.rect_side
                if self.game[i][j] == 0:
                    color = 'white'
                elif self.game[i][j] == 1:
                    color = 'black'
                elif self.game[i][j] == 2:
                    color = 'pink'
                elif self.game[i][j] == 3:
                    color = 'red'
                elif self.game[i][j] == 4:
                    color = 'magenta'
                elif self.game[i][j] == 5:
                    color = 'blue'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tag = (i,j))

    def change_rect_color(self, event, value, color):
        item = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)[0]
        tag = self.canvas.gettags(item)
        i,j = int(tag[0]), int(tag[1])
        if self.game[i][j] == 0:
            self.game[i][j] = value
            self.canvas.itemconfig(item, fill=color)
            self.canvas.update()
            
    def mouse_movement(self, event):
        if self.mouse_clicked == True:
            self.change_rect_color(event, 1, 'black')
    
    def mouse_click(self, event):
        if self.mouse_clicked in [2,3]:
            item = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)[0]
            tag = self.canvas.gettags(item)
            i,j = int(tag[0]), int(tag[1])
            self.points.append([i,j])
            self.change_rect_color(event, 2, 'pink')
        else:
            self.change_rect_color(event, 1, 'black')
            self.mouse_clicked = True
    
    def mouse_release(self, event):
        self.mouse_clicked = 3 if self.mouse_clicked == 2 else False

    def find_visited(self):
        neighbors = [[-1,0], [0,-1], [0,1], [1,0]]
        temp_list = []
        for i in range(len(self.unvisited_nodes)):
            for j in range(len(self.unvisited_nodes[0])):
                if self.unvisited_nodes[i][j][0] in (1,2) and [i,j] not in self.visited_nodes:
                    self.visited_nodes.append([i,j])
                    for neighbor in neighbors:
                        if i+neighbor[0] >= 0 and i+neighbor[0] < len(self.unvisited_nodes[0]) and j+neighbor[1] >= 0 and j+neighbor[1] < len(self.unvisited_nodes):
                            if self.unvisited_nodes[i+neighbor[0]][j+neighbor[1]][0] == 0:
                                temp_list.append([i+neighbor[0],j+neighbor[1]])
                                self.unvisited_nodes[i+neighbor[0]][j+neighbor[1]][1] = self.unvisited_nodes[i][j][1] + 1 if self.unvisited_nodes[i][j][1] + 1 < self.unvisited_nodes[i+neighbor[0]][j+neighbor[1]][1] else self.unvisited_nodes[i+neighbor[0]][j+neighbor[1]][1]
                            elif self.unvisited_nodes[i+neighbor[0]][j+neighbor[1]][0] == 3:
                                self.done = True
        
        for node in temp_list:
            self.unvisited_nodes[node[0]][node[1]][0] = 1
            self.game[node[0]][node[1]] = 3
            if self.check_var.get() == 1:
                time.sleep(0.01)
                self.draw_game()
                self.canvas.update()

    def find_path(self, old_i, old_j, i, j):
        pass 

    def Run(self):
        self.unvisited_nodes = [[[0,9999] for j in range(self.width//self.rect_side)] for i in range(self.height//self.rect_side)]

        for i in range(self.height//self.rect_side):
            for j in range(self.width//self.rect_side):
                if self.game[i][j] == 1:
                    self.unvisited_nodes[i][j][0] = 4
        
        self.unvisited_nodes[self.points[0][0]][self.points[0][1]][0] = 2
        self.unvisited_nodes[self.points[0][0]][self.points[0][1]][1] = 0
        self.unvisited_nodes[self.points[1][0]][self.points[1][1]][0] = 3

        self.visited_nodes = []

        self.done = False
     
        while self.done == False:
            self.find_visited()

        #self.find_path(-1,-1,self.points[0][0], self.points[0][1])

        self.draw_game()
        self.canvas.update()

gui = GUI()
