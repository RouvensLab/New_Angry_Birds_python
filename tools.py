#Hier werden die Buttons generiert.
import pygame
import options


class button:
    """
    This class creates a button object\n
        .show() to draw the image\n
        .collidepoint() to to check if the button collides with the mouse coordinate
    """
    def __init__(self, gameobj, picture, pos, size):
        self.gameobj = gameobj
        self.picture = pygame.transform.scale(picture, size)
        self.size = size
        self.pos = pos
        self.button_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def draw_rect_alpha(self,surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

    def show(self):
        self.gameobj.screen.blit(self.picture, self.pos)
        if self.collidepoint():
            #print("Light {}".format(self.get_rect()))
            self.draw_rect_alpha(self.gameobj.screen, (0, 0, 0, 70), self.get_rect())
            
        else:
            pass
        return True

    def collidepoint(self):
        if self.button_rect.collidepoint(self.gameobj.x_mouse,  self.gameobj.y_mouse):
            return True
        else:
            return False

    def get_rect(self):
        return self.pos[0], self.pos[1], self.size[0], self.size[1]

            