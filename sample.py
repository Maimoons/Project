import os
import sys
import math
import random
import pygame as pg


BACKGROUND_COLOR = (40,40,40)
RECT_SIZE = (30,30)
CAPTION = "Block Collision"


class Block(pg.sprite.Sprite):
    def __init__(self,color,position):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect((0,0),RECT_SIZE)
        self.rect.center = position
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill(color)
        self.true_pos = list(self.rect.center)
        self.velocity = [random.randint(-5, 5), random.randint(-5, 5)]
        self.unit_vector = self.get_unit_vector(self.velocity)

    def get_unit_vector(self,vector):
        magnitude = math.hypot(*vector)
        unit = float(vector[0])/magnitude, float(vector[1])/magnitude
        return unit

    def update(self,screen_rect,others):
        self.true_pos[0] += self.velocity[0]
        self.true_pos[1] += self.velocity[1]
        self.rect.center = self.true_pos
        for other in others:
            if other is not self:
                self.collide(other)
        self.collide_walls(screen_rect)

    def collide_walls(self,screen_rect):
        out_left = self.rect.left < screen_rect.left
        out_right = self.rect.right > screen_rect.right
        out_top = self.rect.top < screen_rect.top
        out_bottom = self.rect.bottom > screen_rect.bottom
        if out_left or out_right:
            self.velocity[0] *= -1
        if out_top or out_bottom:
            self.velocity[1] *= -1
        if any((out_left,out_right,out_top,out_bottom)):
            self.constrain(screen_rect)
            self.unit_vector = self.get_unit_vector(self.velocity)

    def collide(self,other):
        changed = False
        while self.rect.colliderect(other):
            self.true_pos[0] -= self.unit_vector[0]
            self.true_pos[1] -= self.unit_vector[1]
            self.rect.center = self.true_pos
            changed = True
        if changed:
            on_right = self.rect.right <= other.rect.left
            on_left = self.rect.left >= other.rect.right
            if on_left or on_right:
                self.velocity[0] *= -1
            else:
                self.velocity[1] *= -1
            self.unit_vector = self.get_unit_vector(self.velocity)

    def constrain(self,screen_rect):
        while not screen_rect.contains(self.rect):
            self.true_pos[0] -= self.unit_vector[0]
            self.true_pos[1] -= self.unit_vector[1]
            self.rect.center = self.true_pos


class Control(object):
    def __init__(self):
        pg.init()
        os.environ["SDL_VIDEO_CENTERED"] = "True"
        pg.display.set_caption(CAPTION)
        self.screen = pg.display.set_mode((500,500))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.blocks = pg.sprite.Group([Block((255,50,50),(50,50)),
                                       Block(pg.Color("cyan"),(240,340)),
                                       Block(pg.Color("yellow"),(180,250)),
                                       Block(pg.Color("green"),(35,450))])

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.blocks.update(self.screen_rect,self.blocks)
            self.screen.fill(BACKGROUND_COLOR)
            self.blocks.draw(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)
            caption = "{} - FPS: {:.2f}".format(CAPTION,self.clock.get_fps())
            pg.display.set_caption(caption)


if __name__ == "__main__":
    Control().main_loop()
    pg.quit()
    sys.exit()
