#test 2
import pygame
from pygame import *
import sys, random, math, fractions

pygame.init()
Screen_Width = 800
Screen_Height = 600

Total_Display = pygame.display.set_mode((Screen_Width, Screen_Height))

clock = pygame.time.Clock()

class Blocks(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        all_sprite_list.add(self)
        block_list.add(self)
        self.image = pygame.Surface((32,32))
        self.rect = self.image.get_rect()
        self.change_y = 0
        self.change_x = 0

    def blockMove (self, cursor_pos_x, cursor_pos_y, player_pos_x, player_pos_y):

        block_vec_x = cursor_pos_x - player_pos_x
        block_vec_y = cursor_pos_y - player_pos_y
        vec_length = math.sqrt(block_vec_x ** 2 + block_vec_y ** 2)
        block_vec_y = (block_vec_y / vec_length) * 5
        block_vec_x = (block_vec_x / vec_length) * 5
        self.change_y += block_vec_y
        self.change_x += block_vec_x

    def update(self):

        self.rect.y += self.change_y
        self.rect.x += self.change_x

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_list.add(self)
        all_sprite_list.add(self)
        self.rect = Rect(400,300,16,16)
        self.image = pygame.Surface((16,16))


all_sprite_list = pygame.sprite.Group()
player_list = pygame.sprite.GroupSingle()
block_list = pygame.sprite.Group()

block = Blocks(16,16)
player = Player()

running = True
while running:
    clock.tick(60)


    for e in pygame.event.get():
        if e == pygame.QUIT:
            Running = False
        if e.type == pygame.KEYDOWN and e.type == pygame.K_ESCAPE:
            running = False

    Mouse_x, Mouse_y = pygame.mouse.get_pos()
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        block = Blocks(16,16)
        block.update()
        block.blockMove(Mouse_x, Mouse_y, player.rect.x, player.rect.y)
        block.rect.x = player.rect.x
        block.rect.y = player.rect.y
    block.update()
    Total_Display.fill((255,0,0))
    for sprite in all_sprite_list:
        pygame.draw.rect(Total_Display,(0,0,0), sprite)
    for blocks in block_list:
        pygame.draw.rect(Total_Display, (0,0,0), block)
    
    pygame.display.flip()