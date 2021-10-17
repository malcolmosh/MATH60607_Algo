from All_class.class_dataset import dataset
import random, pathlib, os, pygame, math

def optimization(data_list):
    for chair in range(0,len(data_list)):
        data_list[chair].append(random.randint(0,1))
        
data = dataset()
print(data.list_files())
data_selection = data.data_selection_list("salle_test50.txt",True)
print(data_selection)

optimization(data_selection)
print(data_selection)


pygame.init()
#Create the screen, Font, Icon
screen = pygame.display.set_mode((900,600))
pygame.display.set_caption("Chairs optimization App")
screen_font = pygame.font.Font((pathlib.Path(__file__).parents[0] / "Font_graphics/roboto/Roboto-Black.ttf"), 50)
icon = pygame.image.load((pathlib.Path(__file__).parents[0] / "Font_graphics/icon.png"))
pygame.display.set_icon(icon)

#Background
background = pygame.image.load(pathlib.Path(__file__).parents[0] / "Font_graphics/background.png").convert()

#Chairs
desk_yellow = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300)) #Take the surface and draw rectangle around it
player_gravity = 0

#Boutons
# button_optimize = pygame.button((0,255,0), 150, 225, 150, 100, "Optimize")
running = True
while running:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if button_optimize.isover(pos):
        #         print("click the button")
        # if event.type == pygame.mousemotion:
        #     if button_optimize.isover(pos):
        #         button_optimize.color = (255,0,0)
        #     else:
        #         button_optimize.color = (0,255,0)
    screen.fill((0,100,100))
    
    #Update the display surface
    pygame.display.update()