import pygame
import math
import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import random


if not pygame.font: print ('Warning, fonts disabled') #if disabled
if not pygame.mixer: print ('Warning, sound disabled') #if disabled

main_dir = os.path.split(os.path.abspath(__file__))[0] #for splitting the absolute path name
data_dir = os.path.join(main_dir, 'data') #for joining the path name with the filename

pygame.init() #calling the module


#    15-112: Principles of Programming and Computer Science
#    Project: Carrom Board
#    Name      : Maimoon
#    AndrewID  : maimoons

#    File Created: 
#    Modification History:
#    Start:10/11/2016 8:00 pm   End:10/11/2016 11:59 pm
#    11/11/2016 :12:00 am        11/11/2016:7:00 am
#    11/11/2016 :1:00 pm        11/11/2016:4:00 pm
#    11/11/2016 :10:00 pm        11/12/2016:3:00 am
#    11/12/2016 :1:00 pm        11/12/2016 :5:00 pm
#    11/12/2016: 8:00 pm          11/12/2016 :12:00 pm

    
#This is a carrom board game.                       
############################################################CLASSES ###############################################################################################################################     
#this is the class for all the carrom pieces
#the attributes of this class includes:
        #self.y=the y cordinate of the midpoint
        #self.x=the x cordinate of the midpoint
        #self.r=the radius of the pieces
        #self.horizontal_velocity=the horizontal velocity of the pieces once it starts moving
        #self.vertical_velocity=the vertical velocity of the pieces once it starts moving
        #self.sinX=the sine of the angle between the direction vector at which the piece is moving and the horizontal
        #self.cosX=the cosine of the angle between the direction vector at which the piece is moving and the horizontal
        #self.tanX=the tangent of the angle between the direction vector at which the piece is moving and the horizontal


friction=0
class piece(): #this is the class for all the carrom pieces   
    def __init__(self,color,y,x,r,idt="default"):
        self.color=color
        self.y=y
        self.x=x
        self.radius=r
        self.horizontal_velocity=0  # the velocity in the horizontal direction
        self.vertical_velocity=0    #the velocity in the vertical direction
        self.velocity=0             #the absolute value of the velocity
        self.sinX=0                 #X is the angle between the vector joining the centerpoints of the: self piece and any piece which collides with it, and the horizontal
        self.cosX=0
        self.tanX=0
        self.id = idt

    #calculates the angle between piece's  midpoint and any point on the board
    # x and y are the midpoint of any piece on the board with which the angle has to be calculated
    #tanX is the tangent of the angle between the line joining the 2 midpoints( this self piece and the colliding piece) and the horizontal
    #hypotenuse is the line joining the 2 midpoints( this self piece and the colliding piece) and the horizontal
    #cosine and sine of the same  angle are calculated based on the hypotenuse. Sine=opposite/hypotenuse, cosine=adjacent/hypotenuse
 
    def angle(self,x,y):   

        self.tanX=float(y-self.y)/float(x-self.x)
        hypotenuse=((y-self.y)**2+(x-self.x) **2)**0.5
        self.cosX=(x-self.x)/hypotenuse
        self.sinX=(y-self.y)/hypotenuse


           
#takes the coorinates x and y through the set pos function
#sets thpse as the self x and y coordinates for the piece so that it appears to be moving with the mouse cursor
    def move_withcursor(self,x,y):  #for hovering the striker with the cursor
        self.x=x
        self.y=y
        
    #u is the initial velocity of the piece which is colliding with this self piece
    #similarly, x and y are the midpoint coordinates of the piece which is colliding with this self piece
    def move(self,u,sin,cos): #for angles between self piece and onther piece which is colliding with it
        
        self.tanX=float(y-self.y)/float(x-self.x)  #calculates the tangent of the angle between the line joining the 2 midpoints( this self piece and the colliding piece) and the horizontal
        hypotenuse=((y-self.y)**2)+((x-self.x) **2)**0.5
        print "Striker u,x,y",u,x,y
        print "Piece u,x,y",self.velocity,self.x,self.y
        print "hyp",hypotenuse
        print "Theta", self.tanX
        self.cosX=cos
        self.sinX=sin
        
        #sinX2,cosX2,tanX2 = self.cosX,self.sinX,1/self.tanX  # sinX2=90-cosX1, cosX2=90-sinX1, tanX2=90-tanX1
        
        self.velocity=u*(24.0/3)#calculates the velocity of this stationary self piece due to collision with a moving particle
        #if self.velocity>50:  
            #self.velocity=0
            #print self.cosX, self.sinX, self.tanX, u
            #print self.cosX, self.sinX,
        
        print "Piece u,x,y",self.velocity,self.x,self.y
        self.horizontal_velocity=(self.velocity) *(self.sinX) #calculating the horizontal and vertical component of the velocity
        self.vertical_velocity=(self.velocity)*(self.cosX)
      
#based on the velocity of the piece that collided with this self piece, the rebound direction and velocity for that colliding piece is calculated
#return the calculated values to set as attribute of the colliding piece object
    def residual(self,u,sin,cos): #the forward velocity of the piece which collided with this self piece
        #sinX2,cosX2,tanX2 = self.sinX,self.cosX,self.tanX  #wrong# sinX2=90-cosX1, cosX2=90-sinX1, tanX2=90-tanX1
        
        velocity=u*(1.0/3)
        sinX2=-sin
        cosX2=-cos
        tanX2=sin*1.0/cos
        
        print velocity, "residual velocity" 
        
        return [velocity, sinX2, cosX2, tanX2] #the angles with which the colliding object should move

    
#This decreases the absolute velocity of the moving pieces based on the direction in which they are moving
#resolves the absolute velocity into horizontal and vertical components
#If the velocity is negative, it decelerates by adding the deceleration (0.5) to the velocity
#vice versa if it is positive, it decreases it by 0.5
    def deceleration(self): # decreases the absolute velocity of the self piece to 0
        global friction
        if friction==1:
            decel=0.25
        if friction==2:
            decel=0.5
        if friction==3:
            decel=0.75
        self.horizontal_velocity=self.velocity *(self.cosX) #calculates vertical and horizontal components
        self.vertical_velocity=self.velocity*(self.sinX)
        print self.horizontal_velocity, self.vertical_velocity, "velocities"
        print self.sinX, self.cosX, "sin, cos"
        if self.velocity == 0:
            return
        
        if self.velocity>0 and self.cosX>0:  # if angle in first quadrant #moving towards North-East
            print 'positive velocity', self.velocity
            self.x=self.x+self.horizontal_velocity #increasing the x midpoint coordinates of this self piece
            self.y=self.y+self.vertical_velocity #increasing the y midpoint coordinates of this self piece
            self.velocity=self.velocity-decel  #decelearating the absolute velocity which affects the horizontal and vertical componenets of the velocity
            if self.velocity<0:
                self.velocity=0


        elif self.velocity>0 and self.cosX<0: #if angle in second quadrant # moving towards North-West
            print 'positive velocity', self.velocity
            self.x=self.x+self.horizontal_velocity #increasing the x midpoint coordinates of this self piece
            self.y=self.y+self.vertical_velocity #increasing the y midpoint coordinates of this self piece
            self.velocity=self.velocity-decel  #decelearating the absolute velocity which affects the horizontal and vertical componenets of the velocity
            if self.velocity<0:
                self.velocity=0
            
            
            
        elif self.velocity<0 and self.cosX<0: # same stuff but in this case the velocity is in negative direction
            print 'negative velocity1',self.velocity
            self.x=self.x+self.velocity
            self.y=self.y+self.velocity
            self.velocity=self.velocity+decel
            if self.velocity>0:
                self.velocity=0
        
            


        else:
            print 'negative velocity2',self.velocity
            self.x=self.x+self.velocity
            self.y=self.y+self.velocity
            self.velocity=self.velocity+decel
            if self.velocity>0:
                self.velocity=0

        
                
        
        
        self.horizontal_velocity=self.velocity *(self.cosX) #calculates the horizontal component of velocity
        self.vertical_velocity=self.velocity*(self.sinX) #calculates the vertical componenet of velocity
        #print math.sin(self.sinX)

        
#this checks if any piece is close to the regions of the four pockets
#and pockets/removes the piece once it is within the region
#if it pockets a black piece, the person whose turn it is gets 10 points
#if it is a white piece, the person whose turn it is gets 20 points
#the piece is only pocketed if it is any piece apart from the striker
#it checks for the closeness to the pocket by taking the midpoints of the pockets
# and checks if the distance between the midpoints of any moving piece and the pockets is less than the sum of the radius of the two
    def pocketting(self): # checks if the piece is within the vicinity of the four pockets 
        global piecelist
        pockets = [(86,84),(885,84),(885,863),(86,863)] # the midpoint coordinates of the four pockets 
        for midpoints in pockets:
            if ((self.x-midpoints[0])**2)+((self.y-midpoints[1])**2)<(15+15)**2 and ((self.x-midpoints[0])**2)+((self.y-midpoints[1])**2)>0: #checks whether within circular loci of the pockets #remember to calculate the right radius 
                if self.color==white:
                    print "my color is white"
                    score_list[player]=score_list[player]+20 #adds to the score the piece which is pocketed #20 pts for white #10 pts for black
                   
                if self.color==black:
                    score_list[player]=score_list[player]+10

                if self!=striker:
                    piecelist.remove(self) #removes the piece from the list when pocketed
                    print "########################################################"
                    print score_list, "scorelist"
                return score_list
                
#this function checks if any moving piece is colliding with the boudaries/edges of the board
#If it either collides with the right or left edge, only the cosX reverses direction
#If it either collides with the top or bottom edge, only the sinX reverses direction
            
    def boundary(self):   #checks if the piece is colliding with the boundaries 
        if self.x>911 or self.x<75 : #1 #the mnax and min for the x coordinated of the game
            if self.x>911:
                self.x=911
            else:
                self.x=75
            self.cosX = -self.cosX
            self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
            self.vertical_velocity=self.velocity*(self.sinX)


        
        if self.y<75 or self.y>941 : #2 #the mnax and min for the x coordinated of the game
            
            if self.y>941:
                self.y=941
            else:
                self.y=75
            self.sinX = -self.sinX
            self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
            self.vertical_velocity=self.velocity*(self.sinX)
        
            
            


################################################# END OF CLASS=PIECE#######################################################################
                           
        
#This is the class background which makes the background for the game
#The init of this class takes the following:
#it takes the input parameter window and the image which needs to be blitted on it
#it then loads the image passed to it
#and fills the entire window with white
        
class Background(pygame.sprite.Sprite): #setting up the window
    def __init__(self,window, imagefile):
        self.windows=window
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(imagefile).convert_alpha() #loads the image 
        window.fill(white) #fills the screen with white initially

#this is a function of the class background
#it draws circles on the window display of the game
    def draw_piece(self, piece): #for drawing pieces on the board
            pygame.draw.circle(self.windows, piece.color,(int(piece.x), int(piece.y)),piece.radius)
##    def draw_rect(self, piece): #for drawing pieces on the board
##        
##        pygame.draw.rect(self.windows, white,[int(piece.x), int(piece.y),30,30])


#this class is for drawing the forcebar on the screen
#the forbar are basically two rectangles
#one rectangle acts as a base
#and the other smaller rectangles moves over it
#the attributes include the x,y starting coordinates and the width and height of the rectangles
class force(pygame.sprite.Sprite):  #forcebar class
    def __init__(self,color,x,y,h,w):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.color=color
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.border=5
        self.dx=3

#once the attributes are set, this is for drawing the forcebar on the screen
    def draw_forcebar(self): #for drawing forcebar on the window
        global window
        pygame.draw.rect(window,self.color,[self.x,self.y,self.width,self.height])

    
#this moves the smaller forebar over the bigger rectangular base
#it does that by increasing the x coordinate of the moving rectangle by 3
#and reversing the x coordinate accordingle when it reaches the end of the base rectangle
    def move_forcebar(self): #for moving the forcebar left to right 
        
        self.x=self.x+self.dx
        if self.x> (840-50): #changing direction when the moving force bar reaches the right end
            self.dx=-self.dx

        if self.x<156: ##changing direction when the moving force bar reaches the left end
            self.dx=-self.dx
               

##############################FUNCTIONS###############################################################                    
#This function is when playing the single player mode
#The x postion for the striker is preset at 200
#for all the possible y positions on the column corresponding to x=200:
#It calculates the gradient i.e tanxU/L of the imaginary line formed by joining the midpoint of the striker and the midpoint of the upper and lower pockets on the right
#It also calculates the intercept(d1 and d2) to have the equations of the two imaginary lines
#Then for every piece on the board, it checks how far apart is every piece from the two lines
#It does it by calculating the perpendicular distance of the piece to the line by first calculating the equation of the perpendicular line
#The gradient of the perpendicular line is simply -1/gradient of the actual line
#The coordinates of the points at which the the line joinging the striker and the pocket, and the its perpendicular bisector line intersect are calculated
#and through pythagoras, the perpendicular distance is calculated
#shortest 1 is the point closest to the first line
#shortest 2 is the point closest to the second line
#whichever of the two is nearer is supposed to be hit
#the x and y coordinates of the piece to hit are returned


def computer(): #of the striker position
    x=200
    shortest1=10000000000000
    shortest2=10000000000000
    global piecelist
    for y in range(250,700):
        #print"in range of y"
        uppperpocket=[885,863]
        lowerpocket=[86,863]
        tanXU=float(uppperpocket[0]-y)/float(uppperpocket[1]-x)
        tanXL=float(lowerpocket[0]-y)/float(lowerpocket[1]-x)

        d1=y-tanXU*x  #y=mx+d  
        d2=y-tanXL*x
        #print d1, d2, "printing"
        

        for i in piecelist:
            print "in piecelist"
            if i!=striker:
                a=i.y
                b=i.x
                #print a, b, "hello"

                c1=a+(1/tanXU)*b #y=(-1/m )x+c
                c2=a+(1/tanXL)*b
                ycoord1=((tanXU**2)/((tanXU**2)+1))*(c1-d1)+d1
                xcoord1=((tanXU**2)/((tanXU**2)+1))/(c1-d1)
                ycoord2=((tanXL**2)/((tanXL**2)+1))*(c2-d2)+d2
                xcoord2=((tanXL**2)/((tanXL**2)+1))/(c2-d2) 

                shortest11= (ycoord1**2)+ xcoord1**2
                #print shortest11, "shortest 11"
                shortest22= (ycoord2**2)+ xcoord2**2
                
                if shortest11<shortest1:
                    #print "inside shortest 11"
                    shortest1=shortest11
                    piecetohit1=i

                if shortest22<shortest2:
                    shortest2=shortest22
                    piecetohit2=i

        if shortest1>shortest2: #checking which of the two close pieces is the closest
            piecetohit=piecetohit2

        else:
            piecetohit=piecetohit1

    print piecetohit.x, piecetohit.y ,"piecetohit.x, piecetohit,y"
    return piecetohit.x, piecetohit.y,200,y
        
                 

#this is a function which essentially draws the board on the screen using the class 'Background' defined above
#it makes an object of the class
#and then blit the image on the screen
#then looping over the list called listofPieces passed as an input parameter, it draws the pieces on the screen
#in the end draws the striker    

def drawboard(listofPieces,striker):
    global window
    boardscreen=Background(window,"carromboard1.jpg") #loads the image via the class Background
    window.blit(boardscreen.image,[0,0]) #blits the loaded image on the white screen

    for piece in listofPieces: #draws the pices from the listofpieces list
        boardscreen.draw_piece(piece)
        
        
    boardscreen.draw_piece(striker)#draws the striker on the board



#different fonts defined for diplaying messages on the screen
smallestfont=font=pygame.font.SysFont("comicsanms",25)
smallfont=font=pygame.font.SysFont("comicsanms",40)
mediumfont=pygame.font.SysFont("comicsanms",90)


#This is a function which is essentially used to display any sort of message on screen    
def messageonscreen(message,color,x,y,font):   #for displaying score on screen

    screen_text=font.render(message, True, color)
    window.blit(screen_text, (x,y))


iscomputer=False #when playing multiplayer, this is set to True
isincomp=False
#This represents the main menu page where you select single or multiplayer
#it goes in to pygame while loop
def main(): #for displaying messages on screen #pygame documentation   
    intro=True
    global iscomputer
    global friction


    
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        window.fill(white)
        screen=Background(window,"home.jpg") #loads the image via the class Background
        window.blit(screen.image,[0,0]) #blits the loaded image on the white screen

        pygame.event.pump()
        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN: # if the enter key is pressed
                        if event.key==pygame.K_RETURN:

                            x,y = pygame.mouse.get_pos()
                            if x<350 and x>125 and y>255 and y<300:
                                intro=False
                                isincomp = True
                                iscomputer=True

                    if event.type == pygame.KEYDOWN: # if the enter key is pressed
                        if event.key==pygame.K_RETURN:
                            x,y = pygame.mouse.get_pos()
                            if x<350 and x>125 and y>300 and y<350:
                                intro=False
                                
                    if event.type == pygame.KEYDOWN: # if the enter key is pressed       
                        if event.key==pygame.K_RETURN:
                            x,y = pygame.mouse.get_pos()
                            if x<500 and x>125  and y>350 and y<400:
                                options.append(Option("friction=1", (125,400),mediumfont))
                                options.append(Option("friction=2", (125,450),mediumfont))
                                options.append(Option("friction=3", (125,500),mediumfont))


                    if event.type == pygame.KEYDOWN: # if the enter key is pressed       
                        if event.key==pygame.K_RETURN:
                            x,y = pygame.mouse.get_pos()
                            if x<350 and x>125  and y>400 and y<450:
                                friction=1
                                length=len(options)
                                del options[length-1]
                                del options[length-2]
                                del options[length-3]

                                
                    if event.type == pygame.KEYDOWN: # if the enter key is pressed       
                        if event.key==pygame.K_RETURN:
                            x,y = pygame.mouse.get_pos()
                            if x<350 and x>125  and y>450 and y<500:
                                friction=2
                                length=len(options)
                                del options[length-1]
                                del options[length-2]
                                del options[length-3]

                                
                    if event.type == pygame.KEYDOWN: # if the enter key is pressed       
                        if event.key==pygame.K_RETURN:
                            x,y = pygame.mouse.get_pos()
                            if x<350 and x>125  and y>500 and y<550:
                                friction=3
                                length=len(options)
                                del options[length-1]
                                del options[length-2]
                                del options[length-3]

            else:
                option.hovered = False
            option.draw()
        pygame.display.update()






        pygame.display.update()
        fps.tick(15)
#for displaying the menu        
class Option:

    hovered = False
    
    def __init__(self, text, pos,font):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()
            
    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        self.rend = font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            
            return (255, 255, 255)
        else:
            return (255, 0, 0)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos


#This function is for detecting collisions between 2 pieces
#as a result of the collisions, the function calls another function which is part of the class piece that calculates the new velocity and direction of the two pieces after collisions
#The moving_list is a list which has all the pices that are moving added to it
#It goes over every piece in the piecelist, and whichever has a non zero velocity, is moving and is added to the the moving_list
#Then every combination of moving_piece and all the pieces in the piece_list, it checks if they are colliding
#it does that by calculating the distance between the two midpoints of the two pieces through pythagoras theorem
#if the moving_piece and the piecelist piece are the same object, nothing happens( this is not a valid combination)
#if the distance is more than 2x the radius, nothing happens since they are not colliding
#else, if the distance is smaller, they are colliding so the new piece starts moving by calling the function piece.move

def collision(): #checks for collisions between pieces
    global piecelist
    global moving_list
    global iscollided
    global CollisonMade
    moving_list=[]
    i = 0
    if CollisonMade:
        return
    for piece in piecelist: # has all the pieces of the game
        v=piece.velocity #finds the self velocity of the piece
        if v!=0: # if the piece is moving at any instance, adds it to the moving pieces list
            #print v, "v"+str(i)
            moving_list.append(piece)

    for moving_piece in moving_list: # goes over the pieces which are moving  
        for piece in piecelist: # for every piece which is moving, checks it with all the pieces for collision
            if piece==moving_piece:
                continue
            else:
                print moving_piece.id," hit ",piece.id
                x1=moving_piece.x #x midpoint of the moving/colliding piece
                y1=moving_piece.y #y midpoint of the moving/colliding piece
                x2=piece.x        #x midpoint of the casual pieces
                y2=piece.y        #y midpoint of the casual pieces
                if ((x1-x2)**2)+((y1-y2)**2)>(30)**2: #checks for the circular loci, if it is within the specifc range of each other
                    print ((x1-x2)**2+(y1-y2)**2)**0.5, "proximity"
                    None#does nothing if the casual piece is not having any collision with that moving piece
                else: #if there is a collision between the moving piece and the stationary casual piece then it moves on the other series of command
##                    if iscollided:
##                        print 'escaped'
##                        return
                    print 'close'
                    CollisonMade = True
                    u=moving_piece.velocity  #gets the moving piece velocity at that instant
                    #moving_piece.x=moving_piece.x+60
                    #moving_piece.y=moving_piece.y+60

                    piece.move(u,moving_piece.sinX,moving_piece.cosX) #calculates how that moving piece velocity affects the stationary pieces velocity and direction
                    piece.deceleration()#starts decelerating the piece which just started moving
                    print "new moving pirce",piece.velocity,piece.sinX,piece.cosX
                    print "Striker velocity",moving_piece.velocity,moving_piece.sinX,moving_piece.cosX
                    
                    moving_piece.velocity=(piece.residual(u,moving_piece.sinX,moving_piece.cosX))[0] #gives back the residual speed and the residual angle at which it should move the object which collided 
                    moving_piece.sinX=(piece.residual(u,moving_piece.sinX,moving_piece.cosX))[1]
                    moving_piece.cosX=(piece.residual(u,moving_piece.sinX,moving_piece.cosX))[2]
                    moving_piece.tanX=(piece.residual(u,moving_piece.sinX,moving_piece.cosX))[3]
                    #moving_piece.velocity = 0
                    iscollided = True
                
##def load_sound(name):  #for loading sounds in the game #pygame documentation- chipmunk
##    class NoneSound:
##        def play(self): pass
##    if not pygame.mixer or not pygame.mixer.get_init():
##        return NoneSound()
##    fullname = os.path.join(data_dir, name)
##    try:
##        sound = pygame.mixer.Sound(fullname)
##    except pygame.error:
##        print ('Cannot load sound: %s' % fullname)
##        raise SystemExit(str(geterror()))
##    return sound                

#for setting the initial velocity of the striker
#based on where the forcebar was when the enter key was pressed
#the forcebar list has 13 predefined velocites
#the 
def roundup(x):   #for rounding up  the x position of the moving force bar when the enter key is pressed
    remainder = x % 60
    if remainder < 30:
        x = int(x / 60) * 60
    else:
        x = int((x + 60) / 60) * 60

    return x
####################################################SETTING UP THE BOARD#########################################################################################################################                          
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
brown=(116,42,42)
fps=pygame.time.Clock() #frames per second

window=pygame.display.set_mode((1200,675)) #making the display window or the surface

CollisonMade = False

screen = pygame.display.set_mode((1200, 675))
#menu_font = pygame.font.Font(None, 40)
smallestfont=font=pygame.font.SysFont("comicsanms",25)
smallfont=font=pygame.font.SysFont("comicsanms",40)
mediumfont=pygame.font.SysFont("comicsanms",90)

options = [Option("CARROM BOARD", (400, 30),mediumfont), Option("SINGLE PLAYER", (125, 255),smallfont),
   Option("MULTI PLAYER", (125, 305),smallfont),Option("COEFFICIENT OF FRICTION", (125, 355),smallestfont)]


main()

window=pygame.display.set_mode((971,941)) #making the display window or the surface

pygame.display.flip() #updates the entire window
pygame.display.set_caption("CARROM BOARD")
boardscreen=Background(window,"carromboard1.jpg")
window.blit(boardscreen.image,[0,0])

##############################################END OF FUNCTIONS#######################################################################################################################################

pr=piece(red,476,491,15)
pw1=piece(white,476-30,491,15,"pw1") #creating piece instances of the class piece #first circle
pw2=piece(white,476+(30*(math.sin(0.52))),491+30*(math.cos(0.52)),15)
pw3=piece(white,476+(30*(math.sin(0.52))),491-30*(math.cos(0.52)),15)

pw4=piece(white,476-2*30*(math.sin(1.04))*(math.sin(0.52))  ,491+2*30*(math.sin(1.04))*(math.cos(0.52)),15) #second circle
pw5=piece(white,476+2*30*(math.sin(1.04))*(math.sin(0.52)),491+2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw6=piece(white,476-2*30*(math.sin(1.04)),491,15)
pw7=piece(white,476+2*30*(math.sin(1.04))*(math.sin(0.52)),491-2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw8=piece(white,476-2*30*(math.sin(1.04))*(math.sin(0.52)),491-2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw9=piece(white,476+2*30*(math.sin(1.04)),491,15)

pb1=piece(black,476+30,491,15) #first circle
pb2=piece(black,476-(30*(math.sin(0.52))),491-30*(math.cos(0.52)),15)
pb3=piece(black,476-(30*(math.sin(0.52))),491+30*(math.cos(0.52)),15)

pb4=piece(black,476,491+2*30*(math.sin(1.04)),15)  #second circle
pb5=piece(black,476-2*30*(math.sin(1.04))*(math.sin(1.047)),491+2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb6=piece(black,476-2*30*(math.sin(1.04))*(math.sin(1.074)),491-2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb7=piece(black,476,491-2*30*(math.sin(1.04)),15)
pb8=piece(black,476+2*30*(math.sin(1.04))*(math.sin(1.074)),491-2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb9=piece(black,476+2*30*(math.sin(1.04))*(math.sin(1.04)),491+2*30*(math.sin(1.04))*(math.cos(1.074)),15)
striker=piece(brown,300,500,15,"Striker")
#piecelist = [striker,pr,pw1,pw2,pw3,pw4,pw5,pw6,pw7,pw8,pw9,pb1,pb2,pb3,pb4,pb5,pb6,pb7,pb8,pb9]
piecelist = [striker,pw1]

forcebarlist=map(lambda x: x/14,[300,310,320,330,340,350,360,370,380,390,400,410,420]) #The preset initial velocity values depending on the forcebar

######################################################INTIALISING##############################################################################################################################################




#striker_sound=load_sound('sound.wav')
isVelocityS=False
gameExit=False #initialising the variable for the game loop
drawforcebar=True
fps=pygame.time.Clock() #frames per second
moving_list=[] # an empty list for storing all the moving pieces at any instance
score_list=[0,0]
player=0
forcebar=force(black,156,800,50,684)
bar=force(white,156,800,50,5)
hover=True

count=True
iscollided = False
#########################################################MAIN LOOP##################################################################################################################################
while not gameExit:#creating a gameloop
    window.fill(white)#applying to surface object/screen the color
    drawboard(piecelist,striker)
    messageonscreen("SCORES:",black,705,60,smallfont)
    messageonscreen("Player 1:"+str(score_list[0]),black,705,90,smallestfont)
    messageonscreen("Player 2:"+str(score_list[1]),black,705,120,smallestfont)
    
    if drawforcebar: #draws and moves the forcebar if drawforce is True
            forcebar.draw_forcebar()
            bar.draw_forcebar()
            bar.move_forcebar()
            
    for event in pygame.event.get(): #getter funcition for events
        if event.type==pygame.QUIT: # if pygame event type is QUIT
            gameExit=True #exiting the game while loop

        if event.type == pygame.KEYDOWN and ((isincomp==False and player==1) or player==0): # if the enter key is pressed
            if event.key==pygame.K_RETURN:
                drawforcebar=False #no need for the forcebar on the screen now
                CollisonMade = False
                x=bar.x-156 #the position in which the moving bar was when the enter key was pressed
                index=roundup(x) #rounds that position to nearest 60
                index=index/60
                u=forcebarlist[index] #compares and retrieves the intial velocity from the pre set list of initial velocities dependent on position of force bar
                
                                        
            
        if hover==True and drawforcebar==False and isVelocityS==False  and len(moving_list)==0 and ((isincomp==False and player==1) or (player==0)): 
            x,y = pygame.mouse.get_pos() #the striker hovers/moves with cursor
            
            striker.move_withcursor(x,y)
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE: #as soon as spacebar is pressed, the striker stops moving and is staionary at that position
                    hover=False
            
        if hover==False and event.type == pygame.MOUSEBUTTONUP and ((isincomp==False and player==1) or (player==0)): #once the striker has been set in position, and the place where the striker should moved is clicked, if calculates the relevant info below
            #striker_sound.play()
            file = 'sound.wav'
            pygame.init()   
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            x,y = pygame.mouse.get_pos() #gets the x,y position where the player wants the striker to move
            striker.velocity=u #sets the initial velocity as the u retrieved from the forcebar above
            isVelocityS=True #makes true- the striker has some velocity now
            striker.angle(x,y) #calculates the angle at which the striker should initially move depending on where the player clicked


        if isincomp==True and player==1: #once the striker has been set in position, and the place where the striker should moved is clicked, if calculates the relevant info below
            #print "yo"
            #striker_sound.play()
            file = 'sound.wav'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            #x,y = pygame.mouse.get_pos() #gets the x,y position where the player wants the striker to move
            striker.velocity=random.choice(forcebarlist) #sets the initial velocity as the u retrieved from the forcebar above
            isVelocityS=True #makes true- the striker has some velocity now

            x,y,hoverx,hovery=computer(  )
            striker.x, striker.y=hoverx,hovery
            striker.angle(x,y) #calculates the angle at which the striker should initially move depending on where the player clicked

                
    if isVelocityS: #once the striker is moving, starts decelerating it       
        collision()
        striker.deceleration()
        
    if isVelocityS==True and striker.velocity==0: #once the striker has stopped moving, it is the next player's turn, and the forcebar reappears
        hover=True
        if ((isincomp==True and player==0 )or isincomp==False ):
            drawforcebar=True
        
        isVelocityS=False
        player=(player+1)%2
        
        #print player, "pla"

    #collision() #in every fps checks for collision

    for pieces in moving_list: #for every piece that is moving, checks whether it is striking the boundary, or is being pocketed
        if pieces.velocity==0:
            moving_list.remove(pieces)
        scorelists=pieces.pocketting()
##        if scorelists!=None:
##            messageonscreen("Player 1"+str(scorelists[0]),black,705,90)
##            messageonscreen("Player 2"+str(scorelists[1]),black,705,120)

        pieces.deceleration()
        
        if isincomp:
            print "boundary called"
        pieces.boundary()

    

            
    
    
    pygame.display.flip() #updates the entire window
    fps.tick(300)

pygame.quit() #uninitialising pygame
#quit() #exits from python
