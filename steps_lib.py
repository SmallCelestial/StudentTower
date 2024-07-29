import pygame
import random


class StepTemplate(pygame.sprite.Sprite):
    """
    Step_template is a father class for other step classes (child classes only add texture)
    
    Attributes:
    ----------
    step_0 (to 5) : pygame.Surface
        a texture of a step
    animation_frames : list[pygame.Surface,...] 
        list of surfaces making animatation
    animation_frames_index : int
        iterator of an animation_frames list

    tall : float
        how many pixels tall a step is
    width : float
        width of a step in pixels
    height : float
        height of a step at which it is spawned/shown
    topLeft : list[x,y]
        a list of two elements, first being x cord, second y cord of topleft corner of step
    biom_id : float
        it identifies the belonging of step to a biom:
        0 - biom not selected yet
        1 - snow_biom
        2 - jungle_biom
        3 - lava_biom
    destruction : bool
        When it is true, the process of destroying (killing) step has already started.

    Methods:
    --------
    __init__():
        Initializes the step with default mechanics (but template doesn't include texture loading).
    initialize_animation_frames():
        Function used by child classes to set animation_frames as list of step_0, step_1...
    destruction_mechanic():
        responsible for animating and destroying step.
    update():
        Updates the step's state.

    """
    def __init__(self, height: int = 0, step_number: int = 0):
        super().__init__()
        self.step_0 = None
        self.step_1 = None
        self.step_2 = None
        self.step_3 = None
        self.step_4 = None
        self.animation_frames = []
        self.animation_frames_index = 0
        self.destruction = False

        self.tall = 0  # initiated value
        self.width = 0  # initiated value
        self.topLeft = [0, 0]  # initiated value
        self.biom_id = 0  # 0 means biom_id not selected yet
        self.number = step_number

        # CHANGES

        #  self.height -> self.absolute_height
        self.absolute_height = height

    def initialize_animation_frames(self):
        self.animation_frames = [self.step_0, self.step_1, self.step_2, self.step_3, self.step_4]

    def destruction_mechanic(self):
        if self.destruction:
            self.animation_frames_index += 0.02
            if self.animation_frames_index < len(self.animation_frames):
                self.image = self.animation_frames[int(self.animation_frames_index)]
            if self.animation_frames_index >= len(self.animation_frames):
                self.kill()

    def update(self):
        self.destruction_mechanic()


class FloorSnowbiom(StepTemplate):
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
    destruction_mechanic():
        This function overrides the destruction_mechanic of parent class, floor doesn't disappear.
    """   

    def __init__(self, height: int = 0, step_number: int = 0):
        super().__init__(height, step_number)
        self.floor_snowbiom_0 = pygame.image.load('resources/floors/floor_snowbiom_0.png').convert_alpha()
        self.animation_frames = [self.floor_snowbiom_0]

        # Do czego to?
        self.tall = 100
        self.width = 1000
        ###

        # Po co ta zmienna
        self.top_left = [0, 900]
        ###

        # Możliwe, że to też niepotrzebne
        self.biom_id = 1
        ###
        
        self.image = self.floor_snowbiom_0
        self.rect = self.image.get_rect(topleft=self.top_left)

    # def destruction_mechanic(self):
    #     pass


class StepSnowbiom(StepTemplate):
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

    def __init__(self, spawn_height: int, step_number: int):
        super().__init__(step_number)
        self.step_0 = pygame.image.load('resources/floors/step_snowbiom_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_snowbiom_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_snowbiom_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_snowbiom_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_snowbiom_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.tall = 50
        self.width = 300
        self.absolute_height = spawn_height
        self.top_left = [random.randint(300, 600), self.absolute_height]
        self.biom_id = 1

        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)


class StepJunglebiom(StepTemplate):
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

    def __init__(self, spawn_height: int, step_number: int):
        super().__init__(step_number)
        self.step_0 = pygame.image.load('resources/floors/step_junglebiom_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_junglebiom_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_junglebiom_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_junglebiom_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_junglebiom_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.tall = 50
        self.width = 300
        self.absolute_height = spawn_height
        self.top_left = [random.randint(300, 600), self.absolute_height]
        self.biom_id = 2

        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)


class StepLavabiom(StepTemplate):
    """
    Step_lavabiom is a class representing step form lavabiom (id = 3)
    
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

    def __init__(self, spawn_height: int, step_number: int):
        super().__init__(step_number)
        self.step_0 = pygame.image.load('resources/floors/step_lavabiom_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_lavabiom_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_lavabiom_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_lavabiom_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_lavabiom_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.tall = 50
        self.width = 300
        self.absolute_height = spawn_height
        self.top_left = [random.randint(300, 600), self.absolute_height]
        self.biom_id = 3

        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)
        