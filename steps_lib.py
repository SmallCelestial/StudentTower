import pygame
import random


class Step_template(pygame.sprite.Sprite):
    """
    Step_template is a father class for other step classes (child classes only add texture)
    
    Attributes:
    ----------
    step_0 (to 5) : pygame.Surface
        a texture of a step
    animation_frames : list[pygame.Surface,...] 
        list of surfaces making animatation
    animation_frames_index : int
        iterator of a animation_frames list 

    tall : float
        how many pixels tall a step is
    width : float
        width of a step in pixels
    height : float
        height of a step at which it is spawned/shown
    topLeft : list[x,y]
        a list of two elements, first being x cord, second y cord of topleft corner of step
    biom_id : float
        it identifies the belonging of step to a biom

        0 - biom not selected yet
        1 - snow_biom
        2 - jungle_biom
        3 - lava_biom

    Methods:
    --------
    __init__():
        Initializes the step with default mechanics (but template doesnt include texture loading).
    initialize_animation_frames():
        Function used by child classes to set animation_frames as list of step_0, step_1...
    animation_mechanic():
        responsible for animating step by choosing image as on of frames from animation_frames
    update():
        Updates the step's state.

    """
    def __init__(self):
        super().__init__()
        self.step_0 = pygame.image.load('resources/floors/step_junglebiom_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_junglebiom_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_junglebiom_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_junglebiom_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_junglebiom_4.png').convert_alpha()
        self.animation_frames = []
        self.animation_frames_index = 0

        self.tall = 0 # initiated value
        self.width = 0 # initiated value
        self.height = 0 # initiated value
        topLeft = [0,0]  # initiated value
        self.biom_id = 0 # 0 means biom_id not selected yet

    def initialize_animation_frames(self):
        self.animation_frames = [self.step_0, self.step_1, self.step_2, self.step_3, self.step_4]

    def animation_mechanic(self):
        self.animation_frames_index += 0.02
        if self.animation_frames_index >= len(self.animation_frames):
            self.animation_frames_index = 0
        self.image = self.animation_frames[int(self.animation_frames_index)]

    def update(self):
        self.animation_mechanic()

class Floor_snowbiom(Step_template):
    """
   Floor_snowbiom is a class representing floor from snowbiom (id = 1)
    
    Attributes:
    ----------
    image : pygame.Surface
        The current image of the step used for rendering.
    rect : pygame.Rect
        The rectangular area defining the step's position and dimensions.

    Methods:
    --------
    __init__():
        Loads textures added to self.animation_frames 
    """   

    def __init__(self, spawn_height: int):
        super().__init__()
        self.floor_snowbiom_0 = pygame.image.load('resources/floors/floor_snowbiom_0.png').convert_alpha()
        self.animation_frames = [self.floor_snowbiom_0]

        self.tall = 100
        self.width = 1000
        self.height = spawn_height
        topLeft = [0, 900]
        self.biom_id = 1 
        
        self.image = self.floor_snowbiom_0
        self.rect = self.image.get_rect(topleft=topLeft)

class Step_snowbiom(Step_template):
    """
    Step_snowbiom is a class representing step from junglebiom (id = 1)
    
    Attributes:
    ----------
    image : pygame.Surface
        The current image of the step used for rendering.
    rect : pygame.Rect
        The rectangular area defining the step's position and dimensions.

    Methods:
    --------
    __init__():
        Loads textures added to self.animation_frames

    """

    def __init__(self, spawn_height: int):
        super().__init__()
        self.step_0 = pygame.image.load('resources/floors/step_snowbiom_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_snowbiom_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_snowbiom_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_snowbiom_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_snowbiom_4.png').convert_alpha()
        print("jungle step init")
        self.initialize_animation_frames()

        self.tall = 50
        self.width = 300
        self.height = spawn_height
        topLeft = [random.randint(300, 600), self.height]
        self.biom_id = 2

        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=topLeft)

class Step_junglebiom(Step_template):
    """
    Step_junglebiom is a class representing step form junglebiom (id = 2)
    
    Attributes:
    ----------
    image : pygame.Surface
        The current image of the step used for rendering.
    rect : pygame.Rect
        The rectangular area defining the step's position and dimensions.

    Methods:
    --------
    __init__():
        Loads textures added to self.animation_frames

    """

    def __init__(self, spawn_height: int):
        super().__init__()
        self.step_0 = pygame.image.load('resources/floors/step_junglebiom_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_junglebiom_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_junglebiom_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_junglebiom_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_junglebiom_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.tall = 50
        self.width = 300
        self.height = spawn_height
        topLeft = [random.randint(300, 600), self.height]

        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=topLeft)





