import pygame
import random


class Step_snowbiom(pygame.sprite.Sprite):
    """
    Step_snowbiom is a class representing texture and rectangle of a step
    
    Attributes:
    ----------
    relative_height : float 
        it describes height on screen, 1000 is at top, 0 is at bottom (contrary to y. positioning)
    falling_speed : float
        how many pixels a sec a step goes down
    height : float
        height of a step
    width : float
        width of a step
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
        iterator of a floor_snowbiom_300 list
    image : pygame.Surface
        The current image of the step used for rendering.
    rect : pygame.Rect
        The rectangular area defining the step's position and dimensions.

    Methods:
    --------
    __init__():
        Initializes the step with default settings and loads the image.
    falling_mechanic():
        makes step fall, based on relative height, and also kill when step out of screen
    animation_mechanic():
        responsible for changing textures for image variable, makes step animated
    update():
        Updates the step's state by  applying gravity.

    """

    def __init__(self, spawn_height: int):
        super().__init__()
        self.floor_snowbiom_300_0 = pygame.image.load('resources/floors/floor_snowbiom_300_0.png').convert_alpha()
        self.floor_snowbiom_300_1 = pygame.image.load('resources/floors/floor_snowbiom_300_1.png').convert_alpha()
        self.floor_snowbiom_300_2 = pygame.image.load('resources/floors/floor_snowbiom_300_2.png').convert_alpha()
        self.floor_snowbiom_300_3 = pygame.image.load('resources/floors/floor_snowbiom_300_3.png').convert_alpha()
        self.floor_snowbiom_300 = [self.floor_snowbiom_300_0, self.floor_snowbiom_300_1, 
                                   self.floor_snowbiom_300_2, self.floor_snowbiom_300_3]
        self.floor_snowbiom_index = 0
        
        self.tall = 50
        self.width = 300
        self.height = spawn_height

        topLeft = [random.randint(300, 600), self.height]
        self.image = self.floor_snowbiom_300_0
        self.rect = self.image.get_rect(topleft=topLeft)

    def animation_mechanic(self):
        self.floor_snowbiom_index += 0.02
        if self.floor_snowbiom_index >= len(self.floor_snowbiom_300):
            self.floor_snowbiom_index = 0
        self.image = self.floor_snowbiom_300[int(self.floor_snowbiom_index)]

    def update(self):
        self.animation_mechanic()


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
    def __init__(self, spawn_height: int):
        super().__init__()
        self.floor_snowbiom_1000_0 = pygame.image.load('resources/floors/floor_snowbiom_1000_0.png').convert_alpha()
        
        self.tall = 100
        self.width = 1000
        self.height = spawn_height

        self.image = self.floor_snowbiom_1000_0
        self.rect = self.image.get_rect(topleft=(0, 900))

    def update(self):
        pass
