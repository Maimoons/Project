import Tkinter

class car(object):
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
    def draw(self,c):
        #draw top
        c.create_rectangle(self.x,self.y,self.x+20,self.y+10)
        #draw body
        c.create_rectangle(self.x-10,self.y+10,self.x+40,self.y+15,fill=self.color)
        #draw wheels
        #back
        c.create_oval(self.x-5,self.y+13,self.x+5,self.y+23,fill="black")
        #front
        c.create_oval(self.x+25,self.y+13,self.x+35,self.y+23,fill="black")
                    

             

#get main window
wnd = Tkinter.Tk()
wnd.title("Quiz 8")
wnd.geometry("400x400")
#create a canvas on the window
c = Tkinter.Canvas(wnd,bg="white")
def newCar():
    global c
    global car1
    global x
    global y
    x=50
    y=50
    car1=car(x,y,"red")
    car1.draw(c)
def initMove():
    global c
    global car1
    global x
    global y
    global wnd
    car1.color="blue"
    dx=3
    x+=dx
    c.delete("all")
    car1=car(x,y,"blue")
    car1.draw(c)
    if x<int(c.cget("width"))-40:
        wnd.after(100,initMove)
    else:
        return None
b1=Tkinter.Button(wnd,text="Draw Car",command=newCar)
b2=Tkinter.Button(wnd,text="Move",command=lambda:wnd.after(100,initMove))
c.pack()
b1.pack()
b2.pack()
wnd.mainloop()
