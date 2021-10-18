import pygame
from All_class.class_menu import *
class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.playing = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.DISPLAY_W = 480
        self.DISPLAY_H = 270
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            print(self.mouse_x, self.mouse_y)
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2,self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
    
    def reset_keys(self):
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False 

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)





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