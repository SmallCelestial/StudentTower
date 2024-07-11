import pygame
import random

class step_snowbiom(pygame.sprite.Sprite):
    """
    ===Atributes===
    relative_height -> it describes height on screen, 1000 is at top, 0 is at bottom (contrary to y. positioning)
    falling_speed ->  how many pixels a sec a step goes down
    height -> height of a step
    width -> wifth of a step
    topLeft -> a list of two elements, first being x cord, second y cord of topleft corner of step
    topRight -> a list of two elements, first being x cord, second y cord of topright corner of step
    floor_snowbiom_300 -> list of all images responsible for animation
    floor_snowbiom_index -> iterator of an floor_snowbiom_300 list

    ===Methods===
    falling_mechcanic() -> makes step fall, based on relative height, and also kill when step out of screen
    animation_mechanic() -> responsible for changing textures for image variable, makes step animated

    """

    def __init__(self):
        super().__init__()
        self.floor_snowbiom_300_0 = pygame.image.load('resources/floors/floor_snowbiom_300_0.png').convert_alpha()
        self.floor_snowbiom_300_1 = pygame.image.load('resources/floors/floor_snowbiom_300_1.png').convert_alpha()
        self.floor_snowbiom_300_2 = pygame.image.load('resources/floors/floor_snowbiom_300_2.png').convert_alpha()
        self.floor_snowbiom_300_3 = pygame.image.load('resources/floors/floor_snowbiom_300_3.png').convert_alpha()
        self.floor_snowbiom_300=[self.floor_snowbiom_300_0,self.floor_snowbiom_300_1,self.floor_snowbiom_300_2,self.floor_snowbiom_300_3]
        self.floor_snowbiom_index=0
        
        self.relative_height = 1000 
        self.falling_speed = 5 
        self.height = 50
        self.width = 300

        self.topLeft = [random.randint(300,600),0]
        self.topRight = [self.topLeft[0]+self.width,self.topLeft[1]]

        self.image = self.floor_snowbiom_300_0
        self.rect = self.image.get_rect(topleft=self.topLeft)

        
    def falling_mechanic(self):
        self.rect.centery += self.falling_speed
        self.relative_height -= self.falling_speed
        if self.relative_height <= 0:
            self.kill()
        
        self.topLeft[1] = self.relative_height #x cords, stay unchanged
        self.topRight[1] = self.relative_height #x cords, stay unchanged
        

    def animation_mehcanic(self):
        self.floor_snowbiom_index += 0.02
        if self.floor_snowbiom_index >= len(self.floor_snowbiom_300):
            self.floor_snowbiom_index = 0
        self.image = self.floor_snowbiom_300[int(self.floor_snowbiom_index)]

    def update(self):
        self.falling_mechanic()
        self.animation_mehcanic()