#Dieser Code alleine ist dafür verantwortlich dass man Levels erstellen kann und auch diese Levels dann erscheinen lassen kann, um diese Levels dann zu spielen.
import pymunk
import pymunk.pygame_util
import pygame
from options import*
import random
from all_textures import *
from tools import *
import time


class game_vicinity:
    def __init__(self, game_obj, the_level):
        def change_coordinates(point):
            return window_size[1]-point
        self.game_obj = game_obj
        self.screen = game_obj.screen
        self.x_mouse = game_obj.x_mouse
        self.y_mouse = game_obj.y_mouse
        self.draw_options = pymunk.pygame_util.DrawOptions(self.game_obj.screen)#temporarily here
        #Generate the space
        self.space = pymunk.Space()
        self.space.gravity = gravitation
        #The Background
        self.background = img_dictionary[the_level[0]]

        #Generate the floor of the world based on the level_infos
        self.floor_hight = change_coordinates(the_level[2])
        floor = pymunk.Segment(self.space.static_body, (0, self.floor_hight), (window_size[0], self.floor_hight), 5)
        floor.elasticity = 0.9
        floor.friction = 0.5
        self.space.add(floor)
        #wals
        floor1 = pymunk.Segment(self.space.static_body, (window_size[0], 0), (window_size[0], window_size[1]), 5)
        floor1.elasticity = 0.9
        floor1.friction = 0.5
        self.space.add(floor1)
        floor2 = pymunk.Segment(self.space.static_body, (0, 0), (0, window_size[1]), 5)
        floor2.elasticity = 0.9
        floor2.friction = 0.5
        self.space.add(floor2)
        floor3 = pymunk.Segment(self.space.static_body, (0, 0), (window_size[0],0), 5)
        floor3.elasticity = 0.9
        floor3.friction = 0.5
        self.space.add(floor3)

        #generate the world with the castle
        self.body_form_list = []
        for object in the_level[1]:
            img = img_dictionary[object[0]]
            pos = (object[1][0]+img.get_size()[0]/2, object[1][1]+img.get_size()[1]/2)
            form = object[2]
            body = pymunk.Body(mass=0.1, moment=10)
            body.position = pos

            if form[0] == "circle":
                shape = pymunk.Circle(body, radius=form[1])
                shape.elasticity = 0.5
                shape.friction = 2
                self.space.add(body, shape)


            if form[0] == "rect":
                shape = pymunk.Poly.create_box(body, form[1], 1)
                shape.elasticity = 0.5
                shape.friction = 4
                self.space.add(body, shape)
            pygame_obj = form
            self.body_form_list.append([img, shape, pygame_obj, object[0]])

        #Generate the Birds
        self.all_birds_list = []
        which_birds = ["yellow_bird", "yellow_bird", "red_bird", "yellow_bird"]
        x_pos_bird = window_size[0]/4
        y_pos_bird = self.floor_hight
        for bird in which_birds:
            x_pos_bird -= 80
            if bird =="red_bird":
                bird_size = red_bird_size#Here
                body = pymunk.Body(mass=0.03, moment=1)
                body.position = (x_pos_bird, y_pos_bird-bird_size[1]/2)
                shape = pymunk.Circle(body, radius=bird_size[1]/2-15)#Hereeeeeee
                shape.elasticity = 0.4
                shape.friction = 2
                self.space.add(body, shape)

            if bird =="yellow_bird":
                bird_size = yellow_bird_size#Here
                body = pymunk.Body(mass=0.03, moment=1)
                body.position = (x_pos_bird, y_pos_bird-bird_size[1]/2)
                shape = pymunk.Circle(body, radius=bird_size[1]/2-15)#Hereeeeeee
                shape.elasticity = 0.4
                shape.friction = 2
                self.space.add(body, shape)

            self.all_birds_list.append([bird, shape, bird_size])

        #Set the first pos of the rope
        pos = (window_size[0]/4, self.floor_hight-sling_size[1])
        self.rope_pos = (int(pos[0]), int(pos[1]+sling_size[1]/6))

        self.turn_of_b = 0
        self.long_click = False
        self.last_long_click = False
        self.impuls_bird = (70,-60)

        self.bird_is_flighing = False
        self.talent_power = False

        #The state which say if i win or lose
        self.state_end = "normal"
        self.round_game = 0

        #Check if the bird touche a pig or if the pig fall from hight place and crash hard
        def draw_collision(arbiter, space, data):
            for c in arbiter.contact_point_set.points:
                r = max(3, abs(c.distance * 5))
                r = int(r)

                p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
                #pygame.draw.circle(data["surface"], pygame.Color("black"), p, r, 1)

                if r > death_s and self.round_game > 100:
                    colision_list = []
                    for object_1 in self.body_form_list:
                        pos = object_1[1].body.position
                        size = object_1[0].get_size()
                        size = (size[0]+10, size[1]+10)
                        what = object_1[3]
                        rect = pygame.Rect(pos[0]-size[0]/2, pos[1]-size[1]/2, size[0], size[1])
                        if rect.collidepoint(p[0], p[1]):
                            if what == "pig":
                                self.body_form_list.remove(object_1)
                                self.space.remove(object_1[1], object_1[1].body)
                            if what in ["plank_1", "plank_2"] and r >= death_s+35:
                                self.body_form_list.remove(object_1)
                                self.space.remove(object_1[1], object_1[1].body)

                #checks if the actual bird hit something or not. If the bird is flighing or not!!
                if self.bird_is_flighing:
                    act_bird = self.all_birds_list[self.turn_of_b-1]
                    name= act_bird[0]
                    size= act_bird[2]
                    pos = act_bird[1].body.position
                    rect = pygame.Rect(pos[0]-size[0]/2, pos[1]-size[1]/2, size[0], size[1])
                    if rect.collidepoint(p[0], p[1]) and r >= 35:
                        self.bird_is_flighing = False
                                

                            


        ch = self.space.add_collision_handler(0, 0)
        ch.data["surface"] = self.game_obj.screen
        ch.post_solve = draw_collision

        #All the buttons
        self.retry_b = button(self, try_again_img, (window_size[0]/4+100, window_size[1]-350), (250,250))
        self.next_b = button(self, play_button_img, (window_size[0]/2, window_size[1]-350), (250,250))



    def run(self):
        counter = 0
        def print_on_screen(text, size, pos):
            text_surface_object = pygame.font.SysFont("resources\Fonts\Arial.ttf",size).render(str(text), True, (255,0,0))
            self.game_obj.screen.blit(text_surface_object, pos)

        def blitRotate(surf, image, pos, originPos, angle):
            # offset from pivot to center
            image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
            offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center  
            # roatated offset from pivot to center
            rotated_offset = offset_center_to_pivot.rotate(-angle)
            # roatetd image center
            rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
            # get a rotated image
            rotated_image = pygame.transform.rotate(image, angle)
            rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
            # rotate and blit the image
            surf.blit(rotated_image, rotated_image_rect)
            # draw rectangle around the image
            #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)
        #Show the castle and the pigs and the background
        #Draw the background
        self.game_obj.screen.blit(self.background, (0,0))
        x_mouse = self.game_obj.x_mouse
        y_mouse = self.game_obj.y_mouse
        self.x_mouse = self.game_obj.x_mouse
        self.y_mouse = self.game_obj.y_mouse
        mouse_click = self.game_obj.mouse_click

        #Backsling
        img_1 = img_dictionary["sling_1"]
        pos = (window_size[0]/4, self.floor_hight-sling_size[1])
        self.game_obj.screen.blit(img_1, pos)

        for obj in self.body_form_list:
            img = obj[0]
            pos = obj[1].body.position
            size = img.get_size()
            angle = obj[1].body.angle*-57.3
            blitRotate(self.game_obj.screen, img, pos, (size[0]/2, size[1]/2), angle)

        #The Birds in the row (at the start)... or in the air or somewhere else
        for birds in self.all_birds_list:
            img = img_dictionary[birds[0]]
            pos = birds[1].body.position
            size = img.get_size()
            angle = birds[1].body.angle*-57.3
            blitRotate(self.game_obj.screen, img, pos, (size[0]/2, size[1]/2), angle)

        #show the sling in the game with the ropes
        img_2 = img_dictionary["sling_2"]
        pos = (window_size[0]/4, self.floor_hight-sling_size[1])
        sling_1_1 = (int(pos[0]+sling_size[0]/1.818), int(pos[1]+sling_size[1]/6))
        sling_2_1 = (int(pos[0]), int(pos[1]+sling_size[1]/6))
        dx, dy = -(sling_1_1[0] - x_mouse), -(sling_1_1[1] - y_mouse)

        

        vec = pymunk.Vec2d(dx,dy)
        
        sling_1_1v = pymunk.Vec2d(int(pos[0]+sling_size[0]/1.818),int(pos[1]+sling_size[1]/6))
        sling_2_1v = pymunk.Vec2d(int(int(pos[0])),int(pos[1]+sling_size[1]/6))
        
        vec_limit = vec.scale_to_length(min(vec.length,300))
        
        #sling_12_2 = (x_mouse, y_mouse)
        pygame.draw.line(self.game_obj.screen, (0,0,0), sling_1_1v, sling_1_1v + vec_limit , 5)
        pygame.draw.line(self.game_obj.screen, (0,0,0), sling_2_1v, sling_1_1v + vec_limit , 5)
        self.game_obj.screen.blit(img_2, pos)


        #Checks which bird is flighing. To activate theier talent with a mouseclick.
        if self.bird_is_flighing and mouse_click:
            if self.all_birds_list[self.turn_of_b-1][0] == "yellow_bird" and self.talent_power:
                shape_bird = self.all_birds_list[self.turn_of_b-1][1]
                shape_bird.body.apply_impulse_at_local_point([40, 0])
                print("fast")
                self.talent_power = False
            print_on_screen("test", 100, (window_size[0]/2-50, 100))
        else:
            self.talent_power = True
        
        if len(self.all_birds_list) > self.turn_of_b:
            #check which bird's turn is and look if it is clicked
            bird_shape_obj = self.all_birds_list[self.turn_of_b]
            #Put the bird at the right position and angle
            bird_shape_obj[1].body.angle = 0
                #place the bird to the sling
            bird_shape_obj[1].body.position = (int(pos[0]+sling_size[0]/3.4482), int(pos[1]+sling_size[1]/6))#pos muss hier von oben kommen!!!!
            bird_shape_obj[1].body.velocity = (0, 0)
            #pygame.draw.circle(self.game_obj.screen, (5,5,5),bird_shape_obj[1].body.position, 10)
                #make a cirkle(Rectangle) around the bird
            pos_bird_center = bird_shape_obj[1].body.position
            actuel_bird_f = pygame.Rect(pos_bird_center[0]-bird_shape_obj[2][0]/2, pos_bird_center[1]-bird_shape_obj[2][1]/2, bird_shape_obj[2][1], bird_shape_obj[2][1])

            #check if clicked and in rect of actuel_bird_f
            if mouse_click and mouse_click != None: 
                if actuel_bird_f.collidepoint(x_mouse, y_mouse):
                    self.first_pos = (x_mouse, y_mouse)
                    self.long_click = True

            #Here to find the last coordinate of the mouse
            if not mouse_click and mouse_click != None:
                if self.last_long_click == True:
                    #Let the bird flying
                    bird_shape_obj[1].body.apply_impulse_at_local_point(self.impuls_bird)
                    self.turn_of_b += 1 
                    self.set_timer = time.time()
                    self.bird_is_flighing = True #Check if the actuel bird is flighing or not.
                    self.long_click = False
            if self.long_click:
                #read position of mouse and calculate the speed of the rope thing and the velocity
                pos = (x_mouse, y_mouse)
                x_delta = (-x_mouse + self.first_pos[0])
                y_delta = (-y_mouse + self.first_pos[1])
                if x_delta > max_delta[0]:
                    x_delta = max_delta[0]
                if x_delta < -max_delta[0]:
                    x_delta = -max_delta[0]
                if y_delta > max_delta[1]:
                    y_delta = max_delta[1]
                if y_delta < -max_delta[1]:
                    y_delta = -max_delta[1]
                self.impuls_bird = x_delta/3, y_delta/3
                #read the nearest position of the mouse, but with the restricion
                bird_shape_obj[1].body.position = sling_1_1v + vec_limit
            self.last_long_click = self.long_click




        else:
            #Check if the pigs won or the birds. When all birds flew, a counter starts to lock if the time is up.
            #This timer is on the screen
            #Counts
        
            counter = round(-self.set_timer+time.time())
            print_on_screen(f"{counter}/{max_time_left}", 100, (window_size[0]/2-50, 100))
        check_pig = None
        for object_1 in self.body_form_list:
            if object_1[-1] == "pig":
                check_pig = True
        if counter>= max_time_left:
            if check_pig:
                self.state_end = "lose"
        if not check_pig:
            self.state_end = "victory"

        if self.state_end == "victory":
            rect = pygame.Rect(window_size[0]/4, 0, window_size[0]/2, window_size[1])
            pygame.draw.rect(self.game_obj.screen, (0,0,0), rect)
            self.retry_b.show()
            self.next_b.show()
            if not mouse_click and mouse_click != None:
                if self.retry_b.collidepoint():
                    self.game_obj.next_state = "new_game"
                if self.next_b.collidepoint():
                    self.game_obj.activ_level +=1
                    self.game_obj.next_state = "new_game"

        if self.state_end == "lose":
            rect = pygame.Rect(window_size[0]/4, 0, window_size[0]/2, window_size[1])
            pygame.draw.rect(self.game_obj.screen, (0,0,0), rect)
            self.retry_b.show()
            self.game_obj.screen.blit(pig_failed, (window_size[0]/4,0))
            if not mouse_click and mouse_click != None:
                if self.retry_b.collidepoint():
                    self.game_obj.next_state = "new_game"


        self.round_game += 1

        #self.space.debug_draw(self.draw_options)
        self.space.step(1/FPS)











class create_new_level:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.screen = game_obj.screen
        self.draw_options = pymunk.pygame_util.DrawOptions(self.game_obj.screen)
    
        #All the things which are in the inventory
        self.haken = button(self, haken_img, (400, 25), (80,80))
        self.background_menu = button(self, background_menu, (50, 440), (200,120))
        self.backg_1 = button(self, background_1, (50, 50), (200,120))
        self.backg_2 = button(self, background_2, (50, 180), (200,120))
        self.backg_3 = button(self, background_3, (50, 310), (200,120))
            #The object for the castle
        self.pig = button(self, pig_failed, (50, 700), pig_size)
        self.plank_1 = button(self, img_dictionary["plank_1"], (50, 770), plank1_size)
        self.plank_2 = button(self, img_dictionary["plank_2"], (50, 850), plank2_size)

        #All the infos which are used to store in the list
        self.floor_hight = 3
        self.all_object = []
        self.level_obj = ["background_menu", self.all_object, self.floor_hight]
        self.long_click = False
        self.last_long_click = False




    def run(self):
             #Show the floor
        def change_coordinates(point):
            return window_size[1]-point

        next_state = None
        self.x_mouse = self.game_obj.x_mouse
        self.y_mouse = self.game_obj.y_mouse
        #Shows the actuel setted background
        image = img_dictionary[self.level_obj[0]]
        self.game_obj.screen.blit(image, (0,0))
        #shows a storage thing at the left (Black)
        pygame.draw.line(self.screen, (255,255,255), (0, change_coordinates(self.floor_hight)), (window_size[0], change_coordinates(self.floor_hight)), 3)
        self.black_rect = pygame.draw.rect(self.game_obj.screen, (10,10,10), pygame.Rect(0, 0, window_size[0]/4, window_size[1]))
        #Shows all the posibel background images (buttons)
        self.haken.show()
        self.background_menu.show()
        self.backg_1.show()
        self.backg_2.show()
        self.backg_3.show()
        #For the castle
        self.pig.show()
        self.plank_1.show()
        self.plank_2.show()


        #check if something was pressed
        mouse_click = self.game_obj.mouse_click
        if not mouse_click and mouse_click != None:
            #The backgrounds
            if self.background_menu.collidepoint():
                name = "background_menu"
                #img_dictionary[name] = pygame.transform.scale(background_menu, window_size) 
                self.level_obj[0] = name
                self.floor_hight = 3

            if self.backg_1.collidepoint():
                name = "background_1"
                #img_dictionary[name] = pygame.transform.scale(background_1, window_size)
                self.level_obj[0] = name
                self.floor_hight = 228

            if self.backg_2.collidepoint():
                name = "background_2"
                #img_dictionary[name] = pygame.transform.scale(background_2, window_size)
                self.level_obj[0] = name
                self.floor_hight = 149

            if self.backg_3.collidepoint():
                name = "background_3"
                #img_dictionary[name] = pygame.transform.scale(background_3, window_size)
                self.level_obj[0] = name
                self.floor_hight = 27


            #When the haken is presses he make the list finish to use it.
            if self.haken.collidepoint():
                self.level_obj[1] = self.all_object
                self.level_obj[2] = self.floor_hight
                next_state = "menu"

        #The castle objects
        if mouse_click and mouse_click != None:
            if self.pig.collidepoint():
                self.long_click = True
                name = "pig"
                shape = ("circle", 15)
                #img_dictionary[name] = pygame.transform.scale(pig_failed, size)
                position = (self.x_mouse, self.y_mouse)
                self.new_obj = [name, position, shape, pig_size]

            if self.plank_1.collidepoint():
                self.long_click = True
                name = "plank_1"
                shape = ("rect", (140, 22))
                position = (self.x_mouse, self.y_mouse)
                self.new_obj = [name, position, shape, plank1_size]

            if self.plank_2.collidepoint():
                self.long_click = True
                name = "plank_2"
                shape = ("rect", (22, 140))
                position = (self.x_mouse, self.y_mouse)
                self.new_obj = [name, position, shape, plank2_size]




        #Here to find the last coordinate of the mouse
        if not mouse_click and mouse_click != None:
            if self.last_long_click == True and self.new_obj[1][0] > window_size[0]/4:
                self.all_object.append(self.new_obj)
            self.long_click = False

        if self.long_click:
            pos = (self.x_mouse, self.y_mouse)
            img_size = self.new_obj[3]
            self.new_obj[1] = (pos[0]-img_size[0]/2, pos[1]-img_size[1]/2)
            image = img_dictionary[self.new_obj[0]]
            self.screen.blit(image, self.new_obj[1])
        #The last state of long click
        self.last_long_click = self.long_click




        #Shows all the objects in the level_obj list
        if len(self.all_object) > 0:
            for object_1 in self.all_object:
                image = img_dictionary[object_1[0]]#Usefull code---------
                self.screen.blit(image, object_1[1])

       



        #puts the data in the hole list obj
        self.level_obj[1] = self.all_object
        return self.level_obj, next_state


