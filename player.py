import pygame
#from steps_lib import *
import random

LEFT_WALL_COORDINATE = 100
RIGHT_WALL_COORDINATE = 900


#spagetti_1
player_group = pygame.sprite.GroupSingle()
falling_floors_group = pygame.sprite.Group()

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
        iterator of an floor_snowbiom_300 list
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

    def __init__(self, spawn_height : int):
        super().__init__()
        self.floor_snowbiom_300_0 = pygame.image.load('resources/floors/floor_snowbiom_300_0.png')#.convert_alpha()
        self.floor_snowbiom_300_1 = pygame.image.load('resources/floors/floor_snowbiom_300_1.png')#.convert_alpha()
        self.floor_snowbiom_300_2 = pygame.image.load('resources/floors/floor_snowbiom_300_2.png')#.convert_alpha()
        self.floor_snowbiom_300_3 = pygame.image.load('resources/floors/floor_snowbiom_300_3.png')#.convert_alpha()
        self.floor_snowbiom_300 = [self.floor_snowbiom_300_0, self.floor_snowbiom_300_1, self.floor_snowbiom_300_2,
                                   self.floor_snowbiom_300_3]
        self.floor_snowbiom_index = 0
        
        #self.relative_height = 1000 
        self.falling_speed = 2 
        self.tall = 50
        self.width = 300
        self.height = spawn_height

        self.topLeft = [random.randint(300, 600), self.height]
        self.topRight = [self.topLeft[0]+self.width, self.topLeft[1]]

        self.image = self.floor_snowbiom_300_0
        self.rect = self.image.get_rect(topleft=self.topLeft)

    #def falling_mechanic(self):
    #    self.rect.centery += self.falling_speed
    #    self.relative_height -= self.falling_speed
    #    if self.relative_height <= 0:
    #        self.kill()
    #    
    #    self.topLeft[1] = self.relative_height
    #    self.topRight[1] = self.relative_height

    def showing(self, player):
        self.rect.top = 800 - self.height + player.current_height

    def animation_mechanic(self):
        self.floor_snowbiom_index += 0.02
        if self.floor_snowbiom_index >= len(self.floor_snowbiom_300):
            self.floor_snowbiom_index = 0
        self.image = self.floor_snowbiom_300[int(self.floor_snowbiom_index)]

    def update(self):
        #self.falling_mechanic()
        self.showing(player_group.sprite)
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
    def __init__(self, spawn_height : int):
        super().__init__()
        self.floor_snowbiom_1000_0 = pygame.image.load('resources/floors/floor_snowbiom_1000_0.png')#.convert_alpha()
        
        self.relative_height = 1 
        self.falling_speed = 0 
        #self.tall = 100
        self.width = 1000

        self.height = spawn_height

        self.topLeft = [0, self.height]
        self.topRight = [self.topLeft[0]+self.width, self.topLeft[1]]

        self.image = self.floor_snowbiom_1000_0
        self.rect = self.image.get_rect(topleft=(0,900))

    def showing(self, player):
        self.rect.top = 800 -self.height + player.current_height
        #print(self.rect.top)

    def update(self):
        self.showing(player_group.sprite)




class Player(pygame.sprite.Sprite):
    """
    The Player class represents the main character in the game, which can walk, jump, and interact with the game
    environment.

    Attributes:
    -----------
    player_walk : pygame.Surface
        The image representing the player standing.
        TODO: The player should walk instead of standing.
    image : pygame.Surface
        The current image of the player used for rendering.
    rect : pygame.Rect
        The rectangular area defining the player's position and dimensions.
    x_speed : float
        The horizontal speed of the player.
    y_speed : float
        The vertical speed of the player.
    current_height : float
        The current height of the player above the ground.
    max_height : float
        The maximum height the player can reach when jumping in the current area.
    can_jump : bool
        Indicates whether the player is able to jump.

    Methods:
    --------
    __init__():
        Initializes the player with default settings and loads the standing image.
    _jump():
        Handles the jumping logic when the player is on the floor.
    player_input():
        Handles the player's input for movement and jumping.
    apply_gravity():
        Applies gravity to the player and updates their position.
    update():
        Updates the player's state by processing input, applying gravity, and checking floor contact.
    """
    def __init__(self):
        super().__init__()
        self.player_walk = pygame.image.load("resources/Player/player_stand.png")#.convert_alpha()
        self.image = self.player_walk
        self.rect = self.image.get_rect(midbottom=(500, 700))

        self.x_speed = 0
        self.y_speed = 0
        self.current_height = 0
        self.max_height = 0
        self.can_jump = True

        #new parameters
        #self.floor_spawn_cooldown = 60  # time between each step is spawned
        #self.floor_spawn_timer = self.floor_spawn_cooldown  # timer used for measuring time between spawns of steps

        #pygame.time.get_ticks()
        self.nr_of_steps_spawned=5
        self.list_of_steps = [[100,"to_spawn",Floor_snowbiom(100)], [400,"to_spawn",Step_snowbiom(400)],
                            [700,"to_spawn",Step_snowbiom(700)], [1000,"to_spawn",Step_snowbiom(1000)],
                            [1200,"to_spawn",Step_snowbiom(1200)], [1600,"to_spawn",Step_snowbiom(1600)]]


    def _jump(self):
        if self.can_jump:
            self.y_speed = -10
            self.can_jump = False

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self._jump()
        if keys[pygame.K_LEFT] and self.rect.left > LEFT_WALL_COORDINATE:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < RIGHT_WALL_COORDINATE:
            self.rect.x += 5

    def apply_gravity(self):
        if self.y_speed < 10 and not self.can_jump:  # max gravity strength
            self.y_speed += 0.2  # gravity strength

        self.rect.centery += self.y_speed

    def height_status(self):
        self.current_height -= self.y_speed
        self.max_height = max(self.max_height, self.current_height)

    def spawning_steps(self):  # function responsible for cyclic spawning falling steps
        
       for iter in range(0,self.nr_of_steps_spawned):
           if self.list_of_steps[iter][0] < self.current_height + 1000 and self.list_of_steps[iter][1] == "to_spawn":
               self.list_of_steps[iter][1] = "spawned"
               falling_floors_group.add(self.list_of_steps[iter][2])

           
           

    def contact_with_steps(self, steps):
        flag_1 = False
        for step in steps:
            if (step.rect.top + 15 >= self.rect.bottom >= step.rect.top - 5 and
                    step.topLeft[0] <= self.rect.centerx <= step.topRight[0] and
                    self.y_speed >= 0):
                self.can_jump = True
                self.rect.bottom = step.rect.top
                self.y_speed = 0
                flag_1 = True
        if not flag_1:
            self.can_jump = False  

    #def time_actualisation(self):
    #    self.time_ = pygame.time.get_ticks()     
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.height_status()
        print(f"{self.current_height}_{self.can_jump}")  # for testing purposes
        self.spawning_steps()
        self.contact_with_steps(falling_floors_group)
        #self.time_actualisation()

#spagetii_2
player_group.add(Player())

# I need to change
class Intro(pygame.sprite.Sprite):
    def __init__(self, main_screen: pygame.Surface):
        super().__init__()
        self.main_screen = main_screen
        self.image = pygame.image.load('resources/backgrounds/intro_background.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (1000, 800))
        self.rect = self.image.get_rect()
        self.rect.center = main_screen.get_rect().center
        self.play_button = False

        self.play_image = pygame.image.load('resources/backgrounds/PlayButtonHighlight.png').convert_alpha()
        self.play_image = pygame.transform.scale(self.play_image, (300, 200))
        self.play_image_rect = self.play_image.get_rect(bottomleft=(150, 500))

        self.help_image = pygame.image.load('resources/backgrounds/HelpButtonHighlight.png').convert_alpha()
        self.help_image = pygame.transform.scale(self.help_image, (300, 200))
        self.help_image_rect = self.help_image.get_rect(bottomleft=(150, 650))

        self.quit_image = pygame.image.load('resources/backgrounds/QuitButtonHighlight.png').convert_alpha()
        self.quit_image = pygame.transform.scale(self.quit_image, (300, 200))
        self.quit_image_rect = self.quit_image.get_rect(bottomleft=(150, 800))

        self.tower_image = pygame.image.load('resources/backgrounds/skyscraper.png').convert_alpha()
        self.tower_image_rect = self.quit_image.get_rect(center=(600, 300))

        self.image.blit(self.play_image, self.play_image_rect)
        self.image.blit(self.help_image, self.help_image_rect)
        self.image.blit(self.quit_image, self.quit_image_rect)
        self.image.blit(self.tower_image, self.tower_image_rect)

        self.main_screen.blit(self.image, self.rect)

    def check_buttons(self):
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_state[0] == 1:
            if self.play_image_rect.collidepoint(mouse_pos):
                self.play_button = True
            elif self.help_image_rect.collidepoint(mouse_pos):
                print("I can't help you")
            elif self.quit_image_rect.collidepoint(mouse_pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        self.check_buttons()