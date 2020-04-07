from tkinter import *
class GUI:
    def __init__(self):
        self.width = 1000
        self.height = 1000
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
                color = 'white' if self.game[i][j] == 0 else 'black'
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

    def Run(self):
        pass

gui = GUI()
