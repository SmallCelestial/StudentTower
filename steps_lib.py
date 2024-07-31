import pygame
import random 
from constants import LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE

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
    step_height : float
        height of a step at which it is spawned/shown
    step_number : int
        number of steps spawned under this certain step
    top_left : [int, int]
        first number is a coordinate x of the topLeft corner of a step,
        second number is a coordinate y of the topLeft corner of a step
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
    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__()
        self.step_0 = None
        self.step_1 = None
        self.step_2 = None
        self.step_3 = None
        self.step_4 = None
        self.animation_frames = []
        self.animation_frames_index = 0
        self.destruction = False

        self.top_left = [0, 0]
        self.step_number = spawn_number
        self.step_height = spawn_height

    def initialize_animation_frames(self):
        self.animation_frames = [self.step_0, self.step_1, self.step_2, self.step_3, self.step_4]

    def destruction_mechanic(self):
        if self.destruction and self.step_number != 0:
            self.animation_frames_index += 0.02
            if self.animation_frames_index < len(self.animation_frames):
                self.image = self.animation_frames[int(self.animation_frames_index)]
            if self.animation_frames_index >= len(self.animation_frames):
                self.kill()

    def update(self):
        self.destruction_mechanic()


class FloorSnowbiom(StepTemplate):
    """
   Floor_snowbiom is a class representing floor from snowbiom
    
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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.floor_snowbiom_0 = pygame.image.load('resources/floors/floor_snowbiom_0.png').convert_alpha()
        self.animation_frames = [self.floor_snowbiom_0]

        self.top_left = [0, 900]
        self.image = self.floor_snowbiom_0
        self.rect = self.image.get_rect(topleft=self.top_left)



class StepSnowbiom(StepTemplate):
    """
    Step_snowbiom is a class representing step from snowbiom
    
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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.step_0 = pygame.image.load('resources/floors/step_snowbiom_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_snowbiom_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_snowbiom_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_snowbiom_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_snowbiom_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.top_left = [random.randint(LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE - 300), self.step_height]
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)

class StepSnowbiom250(StepTemplate):
    """
    Step_snowbiom is a class representing step from snowbiom
    
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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.step_0 = pygame.image.load('resources/floors/step_snowbiom250_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_snowbiom250_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_snowbiom250_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_snowbiom250_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_snowbiom250_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.top_left = [random.randint(LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE - 250), self.step_height]
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)

class StepSnowbiom200(StepTemplate):
    """
    Step_snowbiom is a class representing step from snowbiom
    
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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.step_0 = pygame.image.load('resources/floors/step_snowbiom200_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_snowbiom200_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_snowbiom200_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_snowbiom200_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_snowbiom200_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.top_left = [random.randint(LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE - 200), self.step_height]
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)

class StepJunglebiom(StepTemplate):
    """
    Step_junglebiom is a class representing step form junglebiom
    
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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.step_0 = pygame.image.load('resources/floors/step_junglebiom_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_junglebiom_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_junglebiom_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_junglebiom_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_junglebiom_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.top_left = [random.randint(LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE - 300), self.step_height]
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)

class StepJunglebiom250(StepTemplate):
    """
    Step_junglebiom is a class representing step from junglebiom

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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.step_0 = pygame.image.load('resources/floors/step_junglebiom250_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_junglebiom250_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_junglebiom250_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_junglebiom250_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_junglebiom250_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.top_left = [random.randint(LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE - 250), self.step_height]
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)

class StepJunglebiom200(StepTemplate):
    """
    Step_junglebiom is a class representing step from junglebiom

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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.step_0 = pygame.image.load('resources/floors/step_junglebiom200_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_junglebiom200_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_junglebiom200_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_junglebiom200_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_junglebiom200_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.top_left = [random.randint(LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE - 200), self.step_height]
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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.step_0 = pygame.image.load('resources/floors/step_lavabiom_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_lavabiom_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_lavabiom_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_lavabiom_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_lavabiom_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.top_left = [random.randint(LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE - 300), self.step_height]
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)

class StepLavabiom250(StepTemplate):
    """
    Step_lavabiom is a class representing step from lavabiom

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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.step_0 = pygame.image.load('resources/floors/step_lavabiom250_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_lavabiom250_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_lavabiom250_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_lavabiom250_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_lavabiom250_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.top_left = [random.randint(LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE - 250), self.step_height]
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)

class StepLavabiom200(StepTemplate):
    """
    Step_lavabiom is a class representing step from lavabiom

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

    def __init__(self, spawn_height: int, spawn_number: int):
        super().__init__(spawn_height, spawn_number)
        self.step_0 = pygame.image.load('resources/floors/step_lavabiom200_0.png').convert_alpha()
        self.step_1 = pygame.image.load('resources/floors/step_lavabiom200_1.png').convert_alpha()
        self.step_2 = pygame.image.load('resources/floors/step_lavabiom200_2.png').convert_alpha()
        self.step_3 = pygame.image.load('resources/floors/step_lavabiom200_3.png').convert_alpha()
        self.step_4 = pygame.image.load('resources/floors/step_lavabiom200_4.png').convert_alpha()
        self.initialize_animation_frames()

        self.top_left = [random.randint(LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE - 200), self.step_height]
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.top_left)
        