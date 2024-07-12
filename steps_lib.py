import pygame
import random


class Step_snowbiom(pygame.sprite.Sprite):
    """
    Step_snowbiom is a class represeting texture and rectangle of a step 
    
    Atributes:
    ----------
    relative_height : float 
        it describes height on screen, 1000 is at top, 0 is at bottom (contrary to y. positioning)
    falling_speed : float
        how many pixels a sec a step goes down
    height : float
        height of a step
    width : float
        wifth of a step
    topLeft : list[x,y]
        a list of two elements, first being x cord, second y cord of topleft corner of step
    topRight : list[x,y]
        a list of two elements, first being x cord, second y cord of topright corner of step
    
    textures:
    ---------
    floor_snowbiom_300_0 : pygame.Surface
        A texture of a step
    floor_snowbiom_300 : list[pygame.Surface,...] 
        list of all images responsible for animation
    floor_snowbiom_index : int
        iterator of an floor_snowbiom_300 list
    image : pygame.Surface
        The current image of the step used for rendering.
    rect : pygame.Rect
        The rectangular area defining the step's position and dimensions.

    Methods:
    --------
    __init__():
        Initializes the step with default settings and loads the image.
    falling_mechcanic():
        makes step fall, based on relative height, and also kill when step out of screen
    animation_mechanic():
        responsible for changing textures for image variable, makes step animated
    update():
        Updates the step's state by  applying gravity.

    """

    def __init__(self):
        super().__init__()
        self.floor_snowbiom_300_0 = pygame.image.load('resources/floors/floor_snowbiom_300_0.png').convert_alpha()
        self.floor_snowbiom_300_1 = pygame.image.load('resources/floors/floor_snowbiom_300_1.png').convert_alpha()
        self.floor_snowbiom_300_2 = pygame.image.load('resources/floors/floor_snowbiom_300_2.png').convert_alpha()
        self.floor_snowbiom_300_3 = pygame.image.load('resources/floors/floor_snowbiom_300_3.png').convert_alpha()
        self.floor_snowbiom_300 = [self.floor_snowbiom_300_0, self.floor_snowbiom_300_1, self.floor_snowbiom_300_2,
                                   self.floor_snowbiom_300_3]
        self.floor_snowbiom_index = 0
        
        self.relative_height = 1000 
        self.falling_speed = 2 
        self.height = 50
        self.width = 300

        self.topLeft = [random.randint(300, 600), 0]
        self.topRight = [self.topLeft[0]+self.width, self.topLeft[1]]

        self.image = self.floor_snowbiom_300_0
        self.rect = self.image.get_rect(topleft=self.topLeft)

    def falling_mechanic(self):
        self.rect.centery += self.falling_speed
        self.relative_height -= self.falling_speed
        if self.relative_height <= 0:
            self.kill()
        
        self.topLeft[1] = self.relative_height  # x cords, stay unchanged
        self.topRight[1] = self.relative_height  # x cords, stay unchanged

    def animation_mehcanic(self):
        self.floor_snowbiom_index += 0.02
        if self.floor_snowbiom_index >= len(self.floor_snowbiom_300):
            self.floor_snowbiom_index = 0
        self.image = self.floor_snowbiom_300[int(self.floor_snowbiom_index)]

    def update(self):
        self.falling_mechanic()
        self.animation_mehcanic()


class Floor_snowbiom(pygame.sprite.Sprite):
    """
    Step_snowbiom is a class represeting texture and rectangle of a step 
    
    Atributes:
    ----------
    relative_height : float 
        it describes height on screen, 1000 is at top, 0 is at bottom (contrary to y. positioning)
    falling_speed : float
        how many pixels a sec a step goes down
    height : float
        height of a step
    width : float
        wifth of a step
    topLeft : list[x,y]
        a list of two elements, first being x cord, second y cord of topleft corner of step
    topRight : list[x,y]
        a list of two elements, first being x cord, second y cord of topright corner of step
    
    textures:
    ---------
    floor_snowbiom_1000_0 : pygame.Surface
        A texture of a step
    image : pygame.Surface
        The current image of the step used for rendering.
    rect : pygame.Rect
        The rectangular area defining the step's position and dimensions.

    Methods:
    --------
    __init__():
        Initializes the step with default settings and loads the image.
    falling_mechcanic():
        makes step fall, based on relative height, and also kill when step out of screen
    animation_mechanic():
        responsible for changing textures for image variable, makes step animated
    update():
        Updates the step's state by  applying gravity.
    """    
    def __init__(self):
        super().__init__()
        self.floor_snowbiom_1000_0 = pygame.image.load('resources/floors/floor_snowbiom_1000_0.png').convert_alpha()
        
        self.relative_height = 1 
        self.falling_speed = 0 
        self.height = 100
        self.width = 1000

        self.topLeft = [0, 700]
        self.topRight = [self.topLeft[0]+self.width, self.topLeft[1]]

        self.image = self.floor_snowbiom_1000_0
        self.rect = self.image.get_rect(topleft=self.topLeft)

    def update(self):
        pass
