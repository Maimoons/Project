import pygame
pygame.init() #calling the module
black=(0,0,0)
white=(255,255,255)
window=pygame.display.set_mode((800,600)) #making the display window or the surface
class Background(pygame.sprite.Sprite):
    def __init__(self, imagefile, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(imagefile)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

   window.fill(WHITE)
   boardscreen=Background("carromboard1.jpg",[0,0])
   window.blit(boardscreen.image,boardscreen.rect)
   pygame.display.flip() #updates the entire window