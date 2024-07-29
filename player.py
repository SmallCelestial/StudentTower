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
        self.player_facing_forward = pygame.image.load("resources/Player/player_stand.png").convert_alpha()
        self.player_facing_right = pygame.image.load("resources/Player/player_walk_1.png").convert_alpha()
        self.player_facing_left = pygame.transform.flip(self.player_facing_right, True, False)

        self.image = self.player_facing_forward
        self.rect = self.image.get_rect(midbottom=(500, 700))

        self.x_speed = 0
        self.y_speed = 0
        self.current_height = 0
        self.max_height = 0
        self.counter = 0
        self.actual_angle = 0
        self.around_delay_counter = 0
        self.direction = 'forward'
        self.ignore_buttons_counter = {'left': 0, 'right': 0}
        self.can_jump = True
        self.super_jump = False
        self.can_move_horizontally = True

    def _can_process_button(self, button: str) -> bool:
        if self.ignore_buttons_counter[button] > 0:
            self.ignore_buttons_counter[button] -= 1
            return False
        return True

    def _jump(self):
        self.direction = 'forward'
        if self.can_jump:
            self.y_speed = -7
            self.can_jump = False
            if self.x_speed >= 8 or self.x_speed <= -8:
                self.super_jump = True
                self.y_speed -= 5

    def _check_wall_collision(self):
        if self.rect.right > RIGHT_WALL_COORDINATE:
            self.rect.right = RIGHT_WALL_COORDINATE
            self.x_speed = -self.x_speed * 0.75
            self.ignore_buttons_counter['right'] = 5
            self.direction = 'left'
        if self.rect.left < LEFT_WALL_COORDINATE:
            self.rect.left = LEFT_WALL_COORDINATE
            self.x_speed = -self.x_speed * 0.75
            self.ignore_buttons_counter['left'] = 5
            self.direction = 'right'

    def _set_position(self):
        if self.super_jump:
            self.image = pygame.transform.rotate(self.player_facing_forward, self.actual_angle)
        elif self.direction == 'left':
            self.image = self.player_facing_left
        elif self.direction == 'right':
            self.image = self.player_facing_right
        elif self.direction == 'forward':
            self.image = self.player_facing_forward

        self.rect = self.image.get_rect(center=self.rect.center)

    def _turn_around(self):
        if self.around_delay_counter > 0:
            self.around_delay_counter -= 1
        else:
            self.can_move_horizontally = True
            self._set_position()

        if (self.direction == 'left' and self.x_speed > 0) or (self.direction == 'right' and self.x_speed < 0):
            self.x_speed = 0
            self.around_delay_counter = 5
            self.can_move_horizontally = False

    def _move(self):
        if self.direction == 'left':
            self.x_speed = self.x_speed - 0.15
            self.x_speed = max(self.x_speed, -10)
            self.rect.x += self.x_speed
        elif self.direction == 'right':
            self.x_speed += 0.15
            self.x_speed = min(self.x_speed, 10)
            self.rect.x += self.x_speed

    def _slow_down(self):
        if self.x_speed > 0:
            self.x_speed = max(self.x_speed - 0.2, 0)
            if self.x_speed == 0:
                self.direction = 'forward'
                self._set_position()
        elif self.x_speed < 0:
            self.x_speed = min(self.x_speed + 0.2, 0)
            if self.x_speed == 0:
                self.direction = 'forward'
                self._set_position()

        self.rect.x += self.x_speed

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self._jump()

        if keys[pygame.K_LEFT] and self._can_process_button('left'):
            self.direction = 'left'
            self._turn_around()
            if self.can_move_horizontally:
                self._move()

        elif keys[pygame.K_RIGHT] and self._can_process_button('right'):
            self.direction = 'right'
            self._turn_around()
            if self.can_move_horizontally:
                self._move()

        elif not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self._slow_down()

        self._check_wall_collision()
        self._set_position()

    def apply_gravity(self):
        if not self.can_jump:
            if self.y_speed < 5:
                self.y_speed += 0.2
            self.counter += 1
            if self.counter % 5 == 0 and self.super_jump:
                self.actual_angle = (self.actual_angle + 60) % 360
                self._set_position()
            if self.rect.top > 100:
                self.rect.centery += self.y_speed
            if self.rect.top <= 100 and self.y_speed <= 0:
                self.rect.top = 100
            elif self.rect.top <= 100 and self.y_speed > 0:
                self.rect.top += self.y_speed
        else:
            self.actual_angle = 0
            self.counter = 0

    def height_status(self):
        self.current_height -= self.y_speed
        self.max_height = max(self.max_height, self.current_height)

    def reset(self):
        self.x_speed = 0
        self.y_speed = 0
        self.current_height = 0
        self.max_height = 0
        self.counter = 0
        self.actual_angle = 0
        self.around_delay_counter = 0
        self.direction = 'forward'
        self.ignore_buttons_counter = {'left': 0, 'right': 0}
        self.can_jump = True
        self.super_jump = False
        self.can_move_horizontally = True
        self.rect.midbottom = (500, 700)

    def update(self):
        self.player_input()
        self.height_status()
        self.apply_gravity()
        # print(f"{self.y_speed}")  # for testing purposes
