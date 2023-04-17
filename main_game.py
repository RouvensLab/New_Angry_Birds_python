#this is the main game
#Dieser Code fügt das Menu mit dem eigentlichen Spiel und mit dem Levelkreator zusammen.
#so here you have to start the programm

import pygame
import pymunk
from options import *
from tools import *
from all_textures import *
from the_game import *
import pickle

#All global variable which can be changed


class game:
    def __init__(self):
        global window_size
        def load_levels():
            with open (level_directory, 'rb') as fp:
                itemlist = pickle.load(fp)
            return itemlist
        pygame.init()
        # Open a new window
        self.screen = pygame.display.set_mode(window_pos, pygame.FULLSCREEN)
        window_size = self.screen.get_size()
        pygame.display.set_caption("Angry Birds")
        # The clock will be used to control how fast the screen updates
        self.clock = pygame.time.Clock()

        """Load the music"""
        song1 = r'resources\audio\angry-birds.ogg'
        pygame.mixer.music.load(song1)
        pygame.mixer.music.play(-1)

        self.mouse_click = False
        self.state = "Init_game"
        self.next_state ="Init_game"
        self.x_mouse = 0
        self.y_mouse = 0
        self.clock = pygame.time.Clock()

        self.activ_level = 0
        self.all_levels = load_levels()
     

    def run(self):
        def save_levels(itemlist):
            with open(level_directory, 'wb') as fp:
                pickle.dump(itemlist, fp)
        
        def print_on_screen(text, size, pos):
            text_surface_object = pygame.font.SysFont("resources\Fonts\Arial.ttf",size).render(str(text), True, (255,0,0))
            self.screen.blit(text_surface_object, pos)
        running = True
        while running:
            # Input handling
            
            self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
            self.mouse_click = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.next_state== "quit":
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                #checks if a mouse is clicked
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.state == "menu":
                        if self.play_button.collidepoint():
                            self.next_state ="new_game"

                        if self.quit_button.collidepoint():
                            self.next_state ="quit"
                        if self.create_level.collidepoint():
                            self.next_state ="create_new_level"
                        #Change the level
                        if self.plus_button.collidepoint():
                            self.activ_level += 1
                            if self.activ_level > len(self.all_levels)-1:
                                self.activ_level -=1
                        if self.minus_button.collidepoint():
                            self.activ_level -= 1
                            if self.activ_level < 0:
                                self.activ_level = 0

                    if self.state == "game_is_running":
                        if self.pause_button.collidepoint():
                            self.next_state ="break"
                        if self.menu_button.collidepoint():
                            self.next_state ="menu"

                    if self.state == "create_level_running":
                        if self.pause_button.collidepoint():
                            self.next_state ="break"
                        if self.menu_button.collidepoint():
                            self.next_state ="menu"

                    if self.state == "break":
                        if self.quit_button.collidepoint():
                            self.next_state ="quit"
                        if self.fortfahren_button.collidepoint():
                            self.next_state ="game_is_running"
                        if self.menu_button.collidepoint():
                            self.next_state ="menu"


            
                #checks if a mouse is clicked
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click = True

            
            
            #Here are all drawing states
            self.screen.fill((0,0,0)) 
            if self.state == "Init_game":
                self.play_button = button(self, play_button_img, (window_size[0]/2-220, window_size[1]/2-150), (440,300))
                self.quit_button = button(self, quit_button_img, (50, 50), (200,200))
                self.create_level = button(self, create_level_img, (window_size[0]/2-125, window_size[1]/2+175), (250,150))
                self.background_menu_scale = pygame.transform.scale(background_menu, window_size)
                #The plus and minus button
                self.plus_button = button(self, plus_img, (window_size[0]/2+80, window_size[1]/2-250), (80,80))
                self.minus_button = button(self, minus_img, (window_size[0]/2-140, window_size[1]/2-250), (80,80))
                #to return to the menu
                self.menu_button = button(self, kreuz, (10, 10), (50,50))
                
                self.pause_button = button(self, pause_img, (500, 90), (120,65))
                self.fortfahren_button = button(self, fortfahren_button_img, (500, 200), (120,65))
                self.next_state = "menu"
            elif self.state == "menu":
                #Show background
                self.screen.blit(background_menu,(0,0))

                self.play_button.show()
                self.quit_button.show()
                self.create_level.show()
                self.plus_button.show()
                print_on_screen(self.activ_level, 80, (window_size[0]/2-15, window_size[1]/2-240))
                self.minus_button.show()

            elif self.state == "break": #==Pause von dem Spiel
                self.quit_button.show()
                self.fortfahren_button.show()
                self.menu_button.show()

            elif self.state == "new_game":
                try:
                    the_level = self.all_levels[self.activ_level]
                except:
                    self.activ_level = 0
                    the_level = self.all_levels[self.activ_level]
                #The game
                self.vicinity = game_vicinity(self, the_level)
                self.next_state ="game_is_running"
            elif self.state == "game_is_running":

                self.vicinity.run()
                self.pause_button.show()
                self.menu_button.show()

            #Object create level wird gemacht
            elif self.state == "create_new_level":
                self.create_level_n = create_new_level(self)
                self.next_state ="create_level_running"
            elif self.state == "create_level_running":
                level_list, next_s = self.create_level_n.run()
                self.menu_button.show()
                if next_s == "menu":
                    self.all_levels.insert(0, level_list)
                    save_levels(self.all_levels)
                    self.next_state = "menu"



            #Print the actual FPS on the screen
            text_surface_object = pygame.font.SysFont("resources\Fonts\Arial.ttf",25).render("FPS "+str(int(self.clock.get_fps())), True, (255,0,0))
            self.screen.blit(text_surface_object,(50,50))
            pygame.display.update()
            self.state = self.next_state    #Neuer State wird erst am schluss eines durchganges gesetzt
            self.clock.tick(FPS)


if __name__ == '__main__':
    start_game = game()
    start_game.run()