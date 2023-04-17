#Hier sind alle Bilder abgespeichert, um sie dann zu nutzen.

import pygame
from options import *

play_button_img = pygame.image.load(r"resources\images\Play.png")
pig_failed = pygame.transform.scale(pygame.image.load(r"resources\images\pig_failed.png"), (window_size[0]/2, window_size[0]/2))
red_bird_img = pygame.image.load(r"resources\images\red-bird.png")
try_again_img = pygame.image.load(r"resources\images\try_again.png")
pause_img = pygame.image.load(r"resources\images\Pause_button.png")
quit_button_img = pygame.image.load(r"resources\images\Quit.png")
fortfahren_button_img = pygame.image.load(r"resources\images\Fortfahren.png")
create_level_img = pygame.image.load(r"resources\images\Create_Level.png")
haken_img = pygame.image.load(r"resources\images\Haken.png")
kreuz = pygame.image.load(r"resources\images\Kreuz.png")
#all backgrounds
background_menu = pygame.image.load(r"resources\images\Menu_background.png")
background_1 = pygame.image.load(r"resources\images\background.png")
background_2 = pygame.image.load(r"resources\images\background1.jpg")
background_3 = pygame.image.load(r"resources\images\background2.jpg")
#The level_controler
plus_img = pygame.image.load(r"resources\images\Plus.png")
minus_img = pygame.image.load(r"resources\images\Minus.png")
yellow_bird = pygame.image.load(r"resources\images\Gelbervogel.png")

img_dictionary = {
"background_menu": pygame.transform.scale(pygame.image.load(r"resources\images\Menu_background.png"), window_size),
"background_1": pygame.transform.scale(pygame.image.load(r"resources\images\background.png"), window_size),
"background_2": pygame.transform.scale(pygame.image.load(r"resources\images\background1.jpg"), window_size),
"background_3": pygame.transform.scale(pygame.image.load(r"resources\images\background2.jpg"), window_size),
"pig": pygame.transform.scale(pygame.image.load(r"resources\images\pig_failed.png"), pig_size),
"plank_1": pygame.transform.rotate(pygame.transform.scale(pygame.image.load(r"resources\images\column_2.png"),plank1_size), 0),
"plank_2": pygame.transform.scale(pygame.image.load(r"resources\images\column_1.png"), plank2_size),
"red_bird": pygame.transform.scale(pygame.image.load(r"resources\images\red-bird.png"), red_bird_size),
"yellow_bird": pygame.transform.scale(pygame.image.load(r"resources\images\Gelbervogel.png"), yellow_bird_size),


"sling_1": pygame.transform.scale(pygame.image.load(r"resources\images\sling_1.png"), sling_size),
"sling_2": pygame.transform.scale(pygame.image.load(r"resources\images\sling_2.png"), sling_size)

}
