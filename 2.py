import pygame
import math
pygame.init() #calling the module
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
brown=(116,42,42)
window=pygame.display.set_mode((971,941)) #making the display window or the surface

pygame.display.flip() #updates the entire window
pygame.display.set_caption("CARROM BOARD")
#This will be a list that will contain all the sprites we intend to use in our game.
sprites_list = pygame.sprite.Group()
# Add the car to the list of objects


class pockets():
    #clock = pygame.time.Clock()
##    pockets = {'pocket1': [(57,69),(116,60),(116,111),(57,111)],
##               'pocket2': [(856,60),(913,60),(913,116),(856,116)],
##               'pocket3': [(57,847),(57,847),(116,897),(57,897)],
##               'pocket4': [(856,847),(913,847),(913,897),(856,897)]}
    pass


    
                       
        
class piece():
    def __init__(self,color,y,x,r):
        self.color=color
        self.y=y
        self.x=x
        self.radius=r
        self.tanX=""
        self.sinX=""
        self.cosX=""
        self.horizontal_velocity=""
        self.vertical_velocity=""
        self.velocity=0
    def angle(x,y):
        self.tanX=int(y-self.y)/int(self.x-x)
        self.cosX=(1+(tanX)**0.5)**-0.5
        self.sinX=(1-(cosX)**0.5)**0.5
        
        
    def move(sinX2,cosX2,tanX2,u):
        velocity=((cosX2)/(self.cosX))(u)+self.tanX(u/2(((sinX2)/(self.sinX))-((self.cosX *cosX2)/(self.sinX)**2)))
        self.horizontal_velocity=velocity *(self.cosX)
        self.vertical_velocity=velocity*(self.sinX)

        return velocity


    def residual():
        velocity=(u/2)(((sinX2)/(self.sinX))-((self.cosX*cosX2)/(self.sinX)*2))

    def deceleration(velocity):
        
        if velocity>0:
            self.x=self.x+self.horizontal_velocity
            self.y=self.y+self.vertical_velocity
            self.velocity=velocity-3
            
        elif velocity<0:
            self.x=self.x-self.velocity
            self.y=self.y-self.velocity
            velocity=velocity-3
        
        self.horizontal_velocity=velocity *(self.cosX)
        self.vertical_velocity=velocity*(self.sinX)

    def pocketting():
        pockets = [(86,84),(885,84),(885,863),(86,863)]
        for midpoints in pockets:
            if ((self.x-midpoints[0])**2)+((self.y-midpoint[1])**2)==(15+r)**2:
                ispot=True #remove the ball

    def boundary():
        if self.x<15 or self.x>(941-30):
            self.velocity=self.velocity *(-1)

        if self.y<15 or self.x>(971-30):
            self.velocity=self.velocity *(-1)


            
            
        

        
        
        
                
        
    
        
class Background(pygame.sprite.Sprite):
    def __init__(self,window, imagefile):
        self.windows=window
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(imagefile).convert_alpha()
        window.fill(white)

    def draw_piece(self, piece):
        pygame.draw.circle(self.windows, piece.color,(int(piece.x), int(piece.y)),piece.radius)

   
                    
def settingboard():
    global window
    boardscreen=Background(window,"carromboard1.jpg")
    window.blit(boardscreen.image,[0,0])
    piecelist=[]
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
    striker=piece(brown,10,10,15)
    
    
    
    p=boardscreen.draw_piece(pr)
    p=boardscreen.draw_piece(pw1)
    p=boardscreen.draw_piece(pw2)
    p=boardscreen.draw_piece(pw3)
    p=boardscreen.draw_piece(pb1)
    p=boardscreen.draw_piece(pb2)
    p=boardscreen.draw_piece(pb3)
    p=boardscreen.draw_piece(pw4)
    p=boardscreen.draw_piece(pw5)
    p=boardscreen.draw_piece(pw6)
    p=boardscreen.draw_piece(pw7)
    p=boardscreen.draw_piece(pw8)
    p=boardscreen.draw_piece(pw9)   
    p=boardscreen.draw_piece(pb4) 
    p=boardscreen.draw_piece(pb5)
    p=boardscreen.draw_piece(pb6)
    p=boardscreen.draw_piece(pb7)
    p=boardscreen.draw_piece(pb8)
    p=boardscreen.draw_piece(pb9)
    p=boardscreen.draw_piece(striker)

def start():
    if pygame.mouse.get_pressed():
        coord=pygame.mouse.get_pos()

def move():
    pass
    
    
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
        
    
def collision():
    pass

            
                    




gameExit=False #initialising the variable for the game loop
fps=pygame.time.Clock() #frames per second
while not gameExit:#creating a gameloop
    window.fill(white)#applying to surface object/scrren the color
    settingboard()
   
    for event in pygame.event.get(): #getter function for events
        if event.type==pygame.QUIT: # if pygame event type is QUIT
            gameExit=True #exiting the game while loop
            
    pygame.display.flip() #updates the entire window
    fps.tick(60)
    
pygame.quit() #uninitialising pygame
quit() #exits from python
