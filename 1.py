import pygame
pygame.init() #calling the module
black=(0,0,0)
white=(255,255,255)
window=pygame.display.set_mode((971,941)) #making the display window or the surface

pygame.display.flip() #updates the entire window
pygame.display.set_caption("CARROM BOARD")
#This will be a list that will contain all the sprites we intend to use in our game.
sprites_list = pygame.sprite.Group()
# Add the car to the list of objects
sprites_list.add()


    
class pieces(pygame.sprite.Sprite):
    #This class represents the display board. It derives from the "Sprite" class in Pygame.
    
    def __init__(self,filename, width, height):# Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
 
        
        #loading a pciture of the board
        self.image = pygame.image.load(filename).convert_alpha()
 
class piece(pygame.sprite.Sprite):
    def __init__(self, imagefile,location):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagefile)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.allframe=[]

        black = pygame.Surface((80, 80))
        black.blit(self.image, (0, 0), (1, 49, 106, 134))
        white = pygame.Surface((80, 80))
        white.blit(self.image, (0, 0), (40, 90, 106, 134))
        striker = pygame.Surface((106, 134))
        striker.blit(self.image, (0, 0), (1, 49, 107, 142))
        
        
        self.allframe.append(black)
        self.allframe.append(white)
        self.allframe.append(striker)
        
        
class Background(pygame.sprite.Sprite):
    def __init__(self,window, imagefile, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(imagefile).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        window.fill(white)
   

   




gameExit=False #initialising the variable for the game loop
fps=pygame.time.Clock() #frames per second

while not gameExit:#creating a gameloop
    boardscreen=Background(window,"carromboard1.jpg",[0,0])
    window.blit(boardscreen.image,boardscreen.rect)
    piece = pieces("pieces.jpg", 432,394)
    window.blit(piece.image,0,0)
    pygame.display.flip() #updates the entire window
    for event in pygame.event.get(): #getter function for events
        if event.type==pygame.QUIT: # if pygame event type is QUIT
            gameExit=True #exiting the game while loop

    window.fill(white)#applying to surface object/scrren the color


fps.tick(60)
pygame.quit() #uninitialising pygame
quit() #exits from python
