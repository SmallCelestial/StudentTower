import pygame
from random import randint


class Intro:
    """
       The Intro class handles the initial screen of the game.

       Attributes:
       -----------
       main_screen : pygame.Surface
           The surface on which the intro screen and its elements are drawn.
       image : pygame.Surface
           The background image for the intro screen.
       rect : pygame.Rect
           The rectangular area defining the position and dimensions of the background image.
       play_button : bool
           Indicates whether the 'Play' button has been clicked.
       play_image : pygame.Surface
           The image representing the 'Play' button.
       play_image_rect : pygame.Rect
           The rectangular area defining the position and dimensions of the 'Play' button.
       help_image : pygame.Surface
           The image representing the 'Help' button.
       help_image_rect : pygame.Rect
           The rectangular area defining the position and dimensions of the 'Help' button.
       quit_image : pygame.Surface
           The image representing the 'Quit' button.
       quit_image_rect : pygame.Rect
           The rectangular area defining the position and dimensions of the 'Quit' button.
       tower_image : pygame.Surface
           The image of a skyscraper displayed on the intro screen.
       tower_image_rect : pygame.Rect
           The rectangular area defining the position and dimensions of the skyscraper image.

       Methods:
       --------
       __init__(screen: pygame.Surface):
           Initializes the Intro screen with background and button images, and sets their positions.
       check_buttons():
           Checks for mouse clicks on buttons and updates the state or performs actions accordingly.
       draw():
           Draws the background, buttons, and skyscraper image onto the main screen.
       update():
           Updates the intro screen by drawing all elements and checking for button interactions.
       """
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.main_screen = screen
        self.image = pygame.image.load('resources/backgrounds/start_background.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (1000, 800))

        self.rect = self.image.get_rect(center=(500, 400))
        self.play_button = False

        self.play_image = pygame.image.load('resources/buttons/PlayButtonHighlight.png').convert_alpha()
        self.play_image = pygame.transform.scale(self.play_image, (300, 200))
        self.play_image_rect = self.play_image.get_rect(bottomleft=(150, 500))

        self.help_image = pygame.image.load('resources/buttons/HelpButtonHighlight.png').convert_alpha()
        self.help_image = pygame.transform.scale(self.help_image, (300, 200))
        self.help_image_rect = self.help_image.get_rect(bottomleft=(150, 650))

        self.quit_image = pygame.image.load('resources/buttons/QuitButtonHighlight.png').convert_alpha()
        self.quit_image = pygame.transform.scale(self.quit_image, (300, 200))
        self.quit_image_rect = self.quit_image.get_rect(bottomleft=(150, 800))

        self.tower_image = pygame.image.load('resources/backgrounds/skyscraper.png').convert_alpha()
        self.tower_image_rect = self.quit_image.get_rect(center=(613, 300))

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

    def draw(self):
        self.main_screen.blit(self.image, self.rect)
        self.main_screen.blit(self.play_image, self.play_image_rect)
        self.main_screen.blit(self.help_image, self.help_image_rect)
        self.main_screen.blit(self.quit_image, self.quit_image_rect)
        self.main_screen.blit(self.tower_image, self.tower_image_rect)

    def update(self):
        self.draw()
        self.check_buttons()


class RotatePlayer(pygame.sprite.Sprite):
    """
        The RotatePlayer class represents a sprite that rotates around its center.

        Attributes:
        -----------
        original_image : pygame.Surface
            The original image of the player, loaded and scaled to its initial size.
        image : pygame.Surface
            The current image of the player, which is rotated and updated.
        rect : pygame.Rect
            The rectangular area defining the position and dimensions of the player image.
        counter : int
            A counter used to control the rotation frequency of the player image.
        angle : float
            The current rotation angle of the player image.

        Methods:
        --------
        __init__():
            Initializes the RotatePlayer instance by loading the player image, scaling it,
             and setting its initial position and attributes.
        rotate():
            Updates the rotation angle of the player image and rotates it accordingly.
             The image is rotated every 10 update cycles.
        update():
            Calls the rotate method to ensure the player image is updated each frame.
        """

    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('resources/PLayer/player_stand.png').convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, (0.75, 0.75))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(775, 500))
        self.counter = 0
        self.angle = 0

    def rotate(self):
        self.counter += 1
        if self.counter % 10 == 0:
            self.angle = (self.angle + 60) % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=(775, 500))

    def update(self):
        self.rotate()


class Floor(pygame.sprite.Sprite):
    """
       The Floor class represents a platform or floor in the game.
        It is used to create and manage the floor's appearance and movement.

       Attributes:
       -----------
       image : pygame.Surface
           The image representing the floor or platform, loaded and scaled to the appropriate size.
       rect : pygame.Rect
           The rectangular area defining the position and dimensions of the floor image.

       Methods:
       --------
       __init__(leftbottom):
           Initializes the Floor instance by loading the floor image, scaling it,
            and setting its position based on the provided bottom-left coordinates.
       move_up():
           Moves the floor upwards by one pixel.
       update():
           Calls the move_up method to update the floor's position each frame.
       """
    def __init__(self, left_bottom: tuple[int, int]):
        super().__init__()
        self.image = pygame.image.load('resources/floors/step_snowbiom_0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 30))
        self.rect = self.image.get_rect(bottomleft=left_bottom)

    def move_up(self):
        self.rect.centery -= 1

    def update(self):
        self.move_up()


class AllFloors:
    """
        The AllFloors class manages a group of floor sprites in the game.

        Attributes:
        -----------
        floors_group : pygame.sprite.Group
            A group containing all the floor sprites in the game.

        Methods:
        --------
        __init__():
            Initializes the AllFloors instance by creating a group of floor sprites.
        check_steps():
            Checks if any floors have moved out of view (i.e., their bottom edge has moved above the screen).
             If so, removes them from the group and replaces them with new floors at the bottom of the screen.
        update():
            Updates the state of all floor sprites by calling their update methods
             and checks for floors that need to be replaced.
        draw(screen):
            Draws all the floor sprites onto the provided screen surface.
        """
    def __init__(self):
        self.floors_group = pygame.sprite.Group()
        height = 100
        for _ in range(4):
            left = randint(600, 800)
            self.floors_group.add(Floor((left, height)))
            height += 200

    def check_steps(self):
        to_add = []
        for step in self.floors_group:
            if step.rect.bottom <= 0:
                self.floors_group.remove(step)
                left = randint(600, 800)
                floor = Floor((left, 0))
                floor.rect.top = 800
                to_add.append(floor)
        self.floors_group.add(to_add)

    def update(self):
        self.check_steps()
        self.floors_group.update()

    def draw(self, screen):
        self.floors_group.draw(screen)


class Outro:
    """
        The Outro class represents the game over or ending screen.

        Attributes:
        -----------
        level : int
            Maximum level reached by the player in the game.
        max_combo : int
            The highest combo achieved by the player during the game.
        score : int
            The total score accumulated by the player.
        max_score : int
            The highest score achieved by the player across all games.
        main_screen : pygame.Surface
            The surface on which the outro screen is drawn.
        image : pygame.Surface
            The background image for the outro screen.
        rect : pygame.Rect
            The rectangular area defining the position and dimensions of the background image.
        rotate_player_group : pygame.sprite.GroupSingle
            A group containing a single RotatePlayer sprite to show a rotating player on the outro screen.
        restart_image : pygame.Surface
            The image of the restart button.
        restart_image_rect : pygame.Rect
            The rectangular area defining the position and dimensions of the restart button.
        home_image : pygame.Surface
            The image of the home button.
        home_image_rect : pygame.Rect
            The rectangular area defining the position and dimensions of the home button.
        floors_group : AllFloors
            An instance of the AllFloors class to manage and display floor sprites on the outro screen.
        status : str
            The current status of the outro screen, used to handle transitions between game states.

        Methods:
        --------
        __init__(screen):
            Initializes the Outro instance by loading images, setting up the rotate player sprite, floor sprites,
             and defining the screen for rendering.
        display_text(text, font, top_left):
            Renders and displays the given text on the screen at the specified position.
        check_buttons():
            Checks for mouse clicks on buttons and updates the status accordingly to handle user input.
        draw():
            Draws the outro screen, including background image, buttons, rotating player, floors, and game statistics.
        update():
            Updates the state of the rotate player sprite and floors, checks for button clicks.
        """
    def __init__(self, screen: pygame.Surface):

        self.level = 0
        self.max_combo = 0
        self.score = 0
        self.max_score = 0

        self.main_screen = screen
        self.image = pygame.image.load('resources/backgrounds/background.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (1000, 800))
        self.rect = self.image.get_rect(center=(500, 400))

        self.rotate_player_group = pygame.sprite.GroupSingle()
        self.rotate_player_group.add(RotatePlayer())

        self.restart_image = pygame.image.load('resources/buttons/restart.png').convert_alpha()
        self.restart_image = pygame.transform.scale_by(self.restart_image, 2)
        self.restart_image_rect = self.restart_image.get_rect(bottomleft=(200, 600))

        self.home_image = pygame.image.load('resources/buttons/home.png').convert_alpha()
        self.home_image = pygame.transform.scale_by(self.home_image, 2)
        self.home_image_rect = self.home_image.get_rect(bottomleft=(200, 750))

        self.floors_group = AllFloors()

        self.status = "outro"

    def display_text(self, text: str, font: pygame.font.Font, top_left: tuple[int, int]):
        text_surface = font.render(text, True, "Brown")
        text_rect = text_surface.get_rect(topleft=top_left)
        self.main_screen.blit(text_surface, text_rect)

    def check_buttons(self):
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_state[0] == 1:
            if self.restart_image_rect.collidepoint(mouse_pos):
                self.status = "game_on"
            elif self.home_image_rect.collidepoint(mouse_pos):
                self.status = "intro"

    def draw(self):
        self.main_screen.blit(self.image, self.rect)
        self.main_screen.blit(self.restart_image, self.restart_image_rect)
        self.main_screen.blit(self.home_image, self.home_image_rect)
        self.rotate_player_group.draw(self.main_screen)
        self.floors_group.draw(self.main_screen)

        font = pygame.font.SysFont("Comic Sans MS", 75)
        self.display_text("GAME OVER", font, (130, 5))

        font = pygame.font.SysFont("Comic Sans MS", 40)
        self.display_text("Level: {}".format(self.level), font, (180, 150))
        self.display_text("Max combo: {}".format(self.max_combo), font, (180, 200))
        self.display_text("Total score: {}".format(self.score), font, (180, 250))
        self.display_text("Best score: {}".format(self.max_score), font, (180, 300))

    def update(self):
        self.rotate_player_group.update()
        self.floors_group.update()
        self.check_buttons()
        self.draw()
