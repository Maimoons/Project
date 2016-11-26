import random
from Tkinter import*
class Circle:
    colors = ["red","blue","green","yellow","orange","purple","black","pink","white","cyan"]
    def __init__(self,x,y):
        self.r = random.randint(10,20)
        self.color = random.choice(Circle.colors)
        self.x = x
        self.y = y
        self.dx = random.randint(-5,5)
        self.dy = random.randint(-5,5)
        self.timer = random.randint(100,500)
        self.me = None
    def move(self,xlimit,ylimit):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        if self.x > xlimit or self.x<0:
            self.dx = -self.dx
        if self.y > ylimit or self.y<0:
            self.dy = -self.dy
        if self.timer == 0:
            self.color = random.choice(Circle.colors)
            self.timer = random.randint(100,500)
        else:
            self.timer = self.timer - 1
    def draw(self,c):
        if self.me != None:
            c.delete(self.me)
        self.me = c.create_oval(self.x,self.y,self.x+(self.r*2),self.y+(self.r*2),fill=self.color)



wnd2=Tk()
wnd2.geometry("300x300")

w = Canvas(wnd2, width=200, height=100)
w.pack()

##w.create_line(0, 0, 200, 100)
##w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
##
##w.create_rectangle(50, 25, 150, 75, fill="blue")

a=Circle(10,10)
b=Circle(50,50)

a.draw(w)

mainloop()
