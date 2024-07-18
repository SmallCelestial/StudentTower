from steps_lib import *

LEFT_WALL_COORDINATE = 100
RIGHT_WALL_COORDINATE = 900


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
        self.player_walk = pygame.image.load("resources/Player/player_stand.png").convert_alpha()

        self.image = self.player_walk
        self.rect = self.image.get_rect(midbottom=(500, 700))

        self.x_speed = 0
        self.y_speed = 0
        self.current_height = 0
        self.max_height = 0
        self.can_jump = True
        self.super_jump = False
        self.counter = 0
        self.actual_angle = 0

    def _jump(self):
        if self.can_jump:
            self.y_speed = -7
            self.can_jump = False
            if self.x_speed >= 4 or self.x_speed <= -4:
                self.super_jump = True
                self.y_speed -= 5

    def _place_inside_area(self):
        if self.rect.right > RIGHT_WALL_COORDINATE:
            self.rect.right = RIGHT_WALL_COORDINATE
            self.x_speed = 0
        if self.rect.left < LEFT_WALL_COORDINATE:
            self.rect.left = LEFT_WALL_COORDINATE
            self.x_speed = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self._jump()

        if keys[pygame.K_LEFT]:
            self.x_speed = min(self.x_speed - 0.5, 0)
            self.x_speed = max(self.x_speed, -6)
            self.rect.x += self.x_speed

        if keys[pygame.K_RIGHT]:
            self.x_speed = max(self.x_speed + 0.5, 0)
            self.x_speed = min(self.x_speed, 6)
            self.rect.x += self.x_speed

        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            if self.x_speed > 0:
                self.x_speed = max(self.x_speed - 0.2, 0)
            elif self.x_speed < 0:
                self.x_speed = min(self.x_speed + 0.2, 0)
            self.rect.x += self.x_speed

        self._place_inside_area()

    def apply_gravity(self):
        if not self.can_jump:
            if self.y_speed < 5:
                self.y_speed += 0.2
            self.counter += 1
            if self.counter % 5 == 0 and self.super_jump:
                self.actual_angle = (self.actual_angle + 60) % 360
                self.image = pygame.transform.rotate(self.player_walk, self.actual_angle)
                self.rect = self.image.get_rect(center=self.rect.center)
            if self.rect.top <= 100 and self.y_speed < 0:
                pass
            else:
                self.rect.centery += self.y_speed
        else:  # player is on floor
            self.image = self.player_walk
            self.rect = self.image.get_rect(center=self.rect.center)
            self.actual_angle = 0
            self.super_jump = False

    def height_status(self):
        self.current_height -= self.y_speed
        self.max_height = max(self.max_height, self.current_height)

        # self.rect.bottom += self.y_speed

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.height_status()
        # print(f"{self.current_height}_{self.can_jump}_{self.y_speed}")  # for testing purposes
