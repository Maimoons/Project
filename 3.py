import pygame
import math
import os, pygame
from pygame.locals import *
from pygame.compat import geterror


#    15-112: Principles of Programming and Computer Science
#    Project: Carrom Board
#    Name      : Maimoon
#    AndrewID  : maimoons

#    File Created: 
#    Modification History:
#    Start:10/28/2016 8:00 pm   End:10/28/2016 11:59 pm
#    10/29/2016 :12:00 am        10/29/2016:9:00 pm
#    10/30/2016 :8:00 pm        10/30/2016 :9:00 pm
#    10/31/2016: 8:00 pm          10/31/2016 :10:00 pm

    
                       
     
class piece(): #this is the class for all the carrom pieces   
    def __init__(self,color,y,x,r):
        self.color=color
        self.y=y
        self.x=x
        self.radius=r
        self.horizontal_velocity=0  # the velocity in the horizontal direction
        self.vertical_velocity=0    #the velocity in the vertical direction
        self.velocity=0             #the absolute value of the velocity
        self.sinX=0
        self.cosX=0
        self.tanX=0


    def angle(self,x,y):
        self.tanX=float(y-self.y)/float(x-self.x)
        hypotenuse=((y-self.y)**2)+((x-self.x) **2)**0.5
        self.cosX=(x-self.x)/hypotenuse
        self.sinX=(y-self.y)/hypotenuse
        
        
    #u is the initial velocity of the piece which is colliding with this self piece
    #similarly, x and y are the midpoint coordinates of the piece which is colliding with this self piece
    def move(self,u,x,y):
        
        self.tanX=float(y-self.y)/float(x-self.x)  #calculates the tangent of the angle between the line joining the 2 midpoints( this self piece and the colliding piece) and the horizontal
        hypotenuse=((y-self.y)**2)+((x-self.x) **2)**0.5
        self.cosX=(x-self.x)/hypotenuse
        self.sinX=(y-self.y)/hypotenuse
        sinX2,cosX2,tanX2 = self.cosX,self.sinX,1/self.tanX  # sinX2=90-cosX1, cosX2=90-sinX1, tanX2=90-tanX1
        
        self.velocity=((cosX2)/(self.cosX))*(u)+(self.tanX)*((u/2)*(((sinX2)/(self.sinX))-((self.cosX *cosX2)/(self.sinX)**2)))
        if self.velocity>50:
            self.velocity=0
            print self.cosX, self.sinX, self.tanX, u
        self.horizontal_velocity=self.velocity *(self.cosX)
        self.vertical_velocity=self.velocity*(self.sinX)
        #self.x = self.x+x/20
        #self.y = self.y+y/20
##        return [self.velocity,self.sinX,self.cosX]


    def residual(self,u): #the backward velocity of the piece which collided with this self piece
        sinX2,cosX2,tanX2 = self.cosX,self.sinX,1/(self.tanX)  # sinX2=90-cosX1, cosX2=90-sinX1, tanX2=90-tanX1
        
        velocity=(u/2)*(((sinX2)/(self.sinX))-((self.cosX*cosX2)/(self.sinX)*2))
        
        return [velocity, sinX2, cosX2, tanX2]

    def deceleration(self): # decreases the absolute velocity of the self piece to 0
        self.horizontal_velocity=self.velocity *(self.cosX)
        self.vertical_velocity=self.velocity*(self.sinX)
        if self.velocity>0:
            print 'positive velocity'
            self.x=self.x+self.horizontal_velocity #increasing the x midpoint coordinates of this self piece
            self.y=self.y+self.vertical_velocity #increasing the y midpoint coordinates of this self piece
            self.velocity=self.velocity-1  #decelearating the absolute velocity which affects the horizontal and vertical componenets of the velocity
            if self.velocity<0:
                self.velocity=0
            
        elif self.velocity<0: # same stuff but in this case the velocity is in negative direction
            print 'negative velocity'
            self.x=self.x-self.velocity
            self.y=self.y-self.velocity
            self.velocity=self.velocity+1
            if self.velocity>0:
                self.velocity=0

        
        
        self.horizontal_velocity=self.velocity *(self.cosX) #calculates the horizontal component of velocity
        self.vertical_velocity=self.velocity*(self.sinX) #calculates the vertical componenet of velocity
        print math.asin(self.sinX)
##        print 'velocity:'
##        print self.velocity
##        print 'sinX:'
##        print self.sinX
##        print 'cosX:'
##        print self.cosX
##        print 'horizontal velocity:'
##        print self.horizontal_velocity
##        print 'vertical velocity:'
##        print self.vertical_velocity
        
        
##    def pocketting(self): # checks if the piece is within the vicinity of the four pockets 
##        global piecelist
##        pockets = [(86,84),(885,84),(885,863),(86,863)] # the midpoint coordinates of the four pockets 
##        for midpoints in pockets:
##            if ((self.x-midpoints[0])**2)+((self.y-midpoints[1])**2)==(15+r)**2: #checks whether within circular loci of the pockets
##                del(piecelist[getindex()]) #remove the ball

    def boundary(self):
        if self.x<15 or self.x>(941-30):  
            self.horizontal_velocity=self.horizontal_velocity *(-1)
            self.cosX = -self.cosX
            self.tanX = -self.tanX
            self.velocity = (self.horizontal_velocity**2 + self.vertical_velocity**2)**0.5
        if self.y<15 or self.y>(971-30):
            self.vertical_velocity=self.vertical_velocity *(-1)
            self.sinX = -self.sinX
            self.tanX = -self.tanX
            self.velocity = (self.horizontal_velocity**2 + self.vertical_velocity**2)**0.5
        


            
            
        

        
            
                
        
    
        
class Background(pygame.sprite.Sprite):
    def __init__(self,window, imagefile):
        self.windows=window
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(imagefile).convert_alpha()
        window.fill(white)

    def draw_piece(self, piece):
        pygame.draw.circle(self.windows, piece.color,(int(piece.x), int(piece.y)),piece.radius)

   
                    
def drawboard(listofPieces,striker):
    global window
    boardscreen=Background(window,"carromboard1.jpg")
    window.blit(boardscreen.image,[0,0])
    for piece in listofPieces:
        boardscreen.draw_piece(piece)
    boardscreen.draw_piece(striker)
    
    
    
def start():
    if pygame.mouse.get_pressed():
        coord=pygame.mouse.get_pos()


    
def messageonscreen(message,color):
    textSurf, textRect= text_objects(msg,color)
    textRect.center=(display_width/2),(display_height/2)
    window.blit(textSurf, textRect)

def main():
    global fps
    global window
    intro=True
    while intro:
        window.fill(white)
        messageonscreen("hi",white)
        messageonscreen("kjk",black)


        pygame.display.update()
        fps.tick(15)
        
    
def collision(): #checks for collisions between pieces
    global piecelist
    global moving_list
    moving_list=[]
    i = 0
    for piece in piecelist: # has all the pieces of the game
        v=piece.velocity #finds the self velocity of the piece
        if v!=0: # if the piece is moving at any instance, adds it to the moving pieces list
            print v, "v"+str(i)
            moving_list.append(piece)

    for moving_piece in moving_list: # goes over the pieces which are moving  
        for piece in piecelist: # for every piece which is moving, checks it with all the pieces for collision
            if piece==moving_piece:
                continue
            x1=moving_piece.x #x midpoint of the moving/colliding piece
            y1=moving_piece.y #y midpoint of the moving/colliding piece
            x2=piece.x        #x midpoint of the casual pieces
            y2=piece.y        #y midpoint of the casual pieces
            if ((x1-x2)**2)+((y1-y2)**2)>(30)**2: #checks for the circular loci, if it is within the specifc range of each other
                
                pass #does nothing if the casual piece is not having any collision with that moving piece
            else: #if there is a collision between the moving piece and the stationary casual piece then it moves on the other series of command
                print 'close'
                u=moving_piece.velocity  #gets the moving piece velocity at that instant
                piece.move(u,x1,y1) #calculates how that moving piece velocity affects the casual stationary pieces velocity and direction
                piece.deceleration()#starts decelerating the piece which just started moving
                moving_piece.velocity=(piece.residual(u))[0] #gives back the residual speed and the residual angles at which it should moveto the object which collided 
                moving_piece.sinX=(piece.residual(u))[1]
                moving_piece.cosX=(piece.residual(u))[2]
                moving_piece.tanX=(piece.residual(u))[3]
                
'''def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound '''               
                
def forcebar():
    pass
    
    

            
                    


pygame.init() #calling the module
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
brown=(116,42,42)
window=pygame.display.set_mode((971,941)) #making the display window or the surface
pygame.display.flip() #updates the entire window
pygame.display.set_caption("CARROM BOARD")
boardscreen=Background(window,"carromboard1.jpg")
window.blit(boardscreen.image,[0,0])

pr=piece(red,476,491,15)
pw1=piece(white,476-30,491,15)
pw2=piece(white,476+(30*(math.sin(0.52))),491+30*(math.cos(0.52)),15)
pw3=piece(white,476+(30*(math.sin(0.52))),491-30*(math.cos(0.52)),15)
pw4=piece(white,476-2*30*(math.sin(1.04))*(math.sin(0.52)),491+2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw5=piece(white,476+2*30*(math.sin(1.04))*(math.sin(0.52)),491+2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw6=piece(white,476-2*30*(math.sin(1.04)),491,15)
pw7=piece(white,476+2*30*(math.sin(1.04))*(math.sin(0.52)),491-2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw8=piece(white,476-2*30*(math.sin(1.04))*(math.sin(0.52)),491-2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw9=piece(white,476+2*30*(math.sin(1.04)),491,15)    
pb1=piece(black,476+30,491,15)
pb2=piece(black,476-(30*(math.sin(0.52))),491-30*(math.cos(0.52)),15)
pb3=piece(black,476-(30*(math.sin(0.52))),491+30*(math.cos(0.52)),15)
pb4=piece(black,476,491+2*30*(math.sin(1.04)),15)
pb5=piece(black,476-2*30*(math.sin(1.04))*(math.sin(1.047)),491+2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb6=piece(black,476-2*30*(math.sin(1.04))*(math.sin(1.074)),491-2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb7=piece(black,476,491-2*30*(math.sin(1.04)),15)
pb8=piece(black,476+2*30*(math.sin(1.04))*(math.sin(1.074)),491-2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb9=piece(black,476+2*30*(math.sin(1.04))*(math.sin(1.04)),491+2*30*(math.sin(1.04))*(math.cos(1.074)),15)
striker=piece(brown,300,500,15)
piecelist = [striker,pr,pw1,pw2,pw3,pw4,pw5,pw6,pw7,pw8,pw9,pb1,pb2,pb3,pb4,pb5,pb6,pb7,pb8,pb9]


#striker_sound=load_sound('sound.wav')
isVelocityS=False
gameExit=False #initialising the variable for the game loop
fps=pygame.time.Clock() #frames per second
moving_list=[] # an empty list for storing all the moving pieces at any instance 
while not gameExit:#creating a gameloop
    window.fill(white)#applying to surface object/scrren the color
    drawboard(piecelist,striker)
    for event in pygame.event.get(): #getter funcition for events
        if event.type==pygame.QUIT: # if pygame event type is QUIT
            gameExit=True #exiting the game while loop



        #print isVelocityS, len(moving_list)
        if isVelocityS==False and event.type == pygame.MOUSEBUTTONUP and len(moving_list)==0:
            
            #striker_sound.play()
            x,y = pygame.mouse.get_pos()
            striker.velocity=50
            #velocity=striker.move(striker.velocity,x,y)
            isVelocityS=True
            striker.angle(x,y)
    if isVelocityS:       
        striker.deceleration()
    if isVelocityS==True and striker.velocity==0:
        isVelocityS=False
    collision()
    for pieces in moving_list:
        #pieces.pocketting()
        pieces.deceleration()
        pieces.boundary()
                
            
    
    
    pygame.display.flip() #updates the entire window
    fps.tick(60)
pygame.quit() #uninitialising pygame
#quit() #exits from python
