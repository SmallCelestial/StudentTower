import pygame


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


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.height_status()
        print(f"{self.current_height}_{self.can_jump}") # for testing purposes # komentarz


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

        # font = pygame.font.Font(None, 36)
        # text = font.render("Play!", True, pygame.Color('Black'))
        # text_rect = text.get_rect(center=self.image.get_rect().center)
        # self.image.blit(text, text_rect)

        self.play_image = pygame.image.load('resources/backgrounds/PlayButtonHighlight.png').convert_alpha()
        self.play_image = pygame.transform.scale(self.play_image, (300, 200))
        self.play_image_rect = self.play_image.get_rect(bottomleft=(150, 500))

        self.help_image = pygame.image.load('resources/backgrounds/HelpButtonHighlight.png').convert_alpha()
        self.help_image = pygame.transform.scale(self.help_image, (300, 200))
        self.help_image_rect = self.help_image.get_rect(bottomleft=(150, 650))

        self.quit_image = pygame.image.load('resources/backgrounds/QuitButtonHighlight.png').convert_alpha()
        self.quit_image = pygame.transform.scale(self.quit_image, (300, 200))
        self.quit_image_rect = self.quit_image.get_rect(bottomleft=(150, 800))

        #  To remove later
        self.tower_image = pygame.image.load('resources/backgrounds/skyscraper.png').convert_alpha()
        # self.tower_image = pygame.transform.scale(self.quit_image, (300, 200))
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
