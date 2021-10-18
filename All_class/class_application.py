import pygame
import pathlib
import random

class Application():
    def __init__(self, dataset, room_info):
        pygame.init()
        self.app_running = True
        self.screen_width = 800
        self.screen_height = 600
        # self.screen_buffer = 100
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.screen_name = pygame.display.set_caption("Chairs optimization App")
        self.font = pygame.font.Font((pathlib.Path(__file__).parents[1] / "Font_graphics/roboto/Roboto-Black.ttf"), 50)
        self.screen_icon = pygame.image.load((pathlib.Path(__file__).parents[1] / "Font_graphics/icon.png"))
        self.screen_background_surf = pygame.image.load(pathlib.Path(__file__).parents[1] / "Font_graphics/background.png").convert()
        self.display = pygame.Surface((self.screen_width,self.screen_height))
        self.clock = pygame.time.Clock()
        self.dataset = dataset
        self.room_info = room_info #Min_x, Max_x, Min_y, Max_y
        self.chairs_group = pygame.sprite.Group()

        self.app_name = self.font.render("Chairs optimization Application", False, (111,196,169))
        self.app_name_rect = self.app_name.get_rect(center = (400,80))
    def game_loop(self):
        while self.app_running:
            self.screen.blit(self.screen_background_surf, (0,0))
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()   
            self.check_events()
            self.chairs_group.draw(self.screen)
            self.chairs_group.update()
            # self.draw_text('Chairs optimization', 20, self.screen_width/2,self.screen_height/2)
            # self.screen.blit(self.display, (0,0))
            pygame.display.update()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space")
                    self.chairs_group.empty()
                    for chair in self.dataset:
                        chair_x = (chair[1] / self.room_info[0] ) * self.screen_width
                        chair_y = (chair[2] / self.room_info[1] ) * self.screen_height
                        chair_state = chair[3]
                        self.chairs_group.add(Chairs(chair_x, chair_y, chair_state))
                if event.key == pygame.K_RETURN:
                    print("Enter")
                    for chair in self.dataset:
                        chair_x = (chair[1] / self.room_info[0] ) * self.screen_width
                        chair_y = (chair[2] / self.room_info[1] ) * self.screen_height
                        chair_state = 0
                        self.chairs_group.add(Chairs(chair_x, chair_y, chair_state))
                if event.key == pygame.K_BACKSPACE:
                    print("Backspace")
                    self.chairs_group.empty()
                # if event.key == pygame.K_RETURN:
                #     self.START_KEY = True
                # if event.key == pygame.K_BACKSPACE:
                #     self.BACK_KEY = True
                # if event.key == pygame.K_DOWN:
                #     self.DOWN_KEY = True
                # if event.key == pygame.K_UP:
                #     self.UP_KEY = True

class Chairs(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, state=0):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.state = state
        desk_brown = pygame.image.load(pathlib.Path(__file__).parents[1] / "Font_graphics/desk_brown.png").convert_alpha()
        desk_green = pygame.image.load(pathlib.Path(__file__).parents[1] / "Font_graphics/desk_green.png").convert_alpha()
        desk_red = pygame.image.load(pathlib.Path(__file__).parents[1] / "Font_graphics/desk_red.png").convert_alpha()
        desk_yellow = pygame.image.load(pathlib.Path(__file__).parents[1] / "Font_graphics/desk_yellow.png").convert_alpha()
        self.desk_color = [desk_brown, desk_green, desk_red, desk_yellow]
        if self.state == 0 : self.color_index = 0
        elif self.state == 1:   self.color_index = 1
        elif self.state == 2:   self.color_index = 2
        elif self.state == 3:   self.color_index = 3
        self.image = self.desk_color[self.color_index]
        self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
    def destroy(self):
        self.kill()
    # def reset_keys(self):
    #     self.UP_KEY = False
    #     self.DOWN_KEY = False
    #     self.START_KEY = False
    #     self.BACK_KEY = False 

    # def draw_text(self, text, size, x, y):
    #     font = pygame.font.Font(self.font_name, size)
    #     text_surface = font.render(text, True, self.WHITE)
    #     text_rect = text_surface.get_rect()
    #     text_rect.center = (x,y)
    #     self.display.blit(text_surface, text_rect)





# pygame.init()
# #Create the screen, Font, Icon
# screen_height = 400
# screen_width = 800
# screen = pygame.display.set_mode((screen_width,screen_height))
# pygame.display.set_caption("Chairs optimization App")
# use_font = pygame.font.Font((pathlib.Path(__file__).parents[0] / "Font_graphics/roboto/Roboto-Black.ttf"), 50)
# icon = pygame.image.load((pathlib.Path(__file__).parents[0] / "Font_graphics/icon.png"))
# pygame.display.set_icon(icon)

# #Background
# background_surf = pygame.image.load(pathlib.Path(__file__).parents[0] / "Font_graphics/background.png").convert()

# #Chairs
# desk_brown = pygame.image.load(pathlib.Path(__file__).parents[0] / "Font_graphics/desk_brown.png").convert_alpha()
# desk_green = pygame.image.load(pathlib.Path(__file__).parents[0] / "Font_graphics/desk_green.png").convert_alpha()
# desk_red = pygame.image.load(pathlib.Path(__file__).parents[0] / "Font_graphics/desk_red.png").convert_alpha()
# desk_yellow = pygame.image.load(pathlib.Path(__file__).parents[0] / "Font_graphics/desk_yellow.png").convert_alpha()
# desk_color = [desk_brown, desk_green,desk_red,desk_yellow]
# desk_index = 0
# desk_surf = desk_color[desk_index]
# desk_rect= desk_surf.get_rect(midbottom = (80,300)) #Take the surface and draw rectangle around it

# #Color
# color_white = (255,255,255)

# #Room
# room_rect = pygame.Rect(300,300,0,0)
# room = pygame.draw.rect(screen, color_white, room_rect)

# #Options
# button1 = use_font.render("button_1", False, (111,196,169))
# button1_rect = button1.get_rect(center = (400,320))

# button2 = use_font.render("button_2", False, (111,196,169))
# button2_rect = button2.get_rect(center = (400,320))


# optimization_active = False
# #Boutons
# # button_optimize = pygame.button((0,255,0), 150, 225, 150, 100, "Optimize")
# while True:
#     for event in pygame.event.get():
#         pos = pygame.mouse.get_pos()
#         if event.type == pygame.QUIT:
#             exit()
#         if optimization_active == True:
#             print("lets go")
#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         #     if button_optimize.isover(pos):
#         #         print("click the button")
#         # if event.type == pygame.mousemotion:
#         #     if button_optimize.isover(pos):
#         #         button_optimize.color = (255,0,0)
#         #     else:
#         #         button_optimize.color = (0,255,0)
#     if optimization_active == True:
#         screen.fill((0,100,0))
#         screen.blit(button1,button1_rect)
#     else:
#         screen.fill((100,0,0))
#         screen.blit(button2,button2_rect)
#     #Update the display surface
#     pygame.display.update()