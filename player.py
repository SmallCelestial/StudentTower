import pygame

LEFT_WALL_COORDINATE = 125
RIGHT_WALL_COORDINATE = 875


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk = pygame.image.load("resources/Player/player_stand.png").convert_alpha()

        self.image = self.player_walk  # jakbys zmienial to napisz
        self.rect = self.image.get_rect(midbottom=(500, 200))  # jakbys zmienial to napisz

        # basic_parameters
        self.x_speed = 0
        self.y_speed = 0
        self.current_height = 0
        self.max_height = 0
        self.floor_under_legs_status = True  # if true player stands on floor and can jump

    def _jump(self):
        if self.floor_under_legs_status:
            self.y_speed = -10
            self.floor_under_legs_status = False

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self._jump()
        if keys[pygame.K_LEFT] and self.rect.left > LEFT_WALL_COORDINATE:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < RIGHT_WALL_COORDINATE:
            self.rect.x += 5

    def gravity_function(self):
        if self.rect.bottom >= 700 and self.current_height == 0:
            self.rect.bottom = 700

        if self.y_speed < 10:  # max garivty strength
            self.y_speed += 0.2  # gravity strength

        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

    def contact_with_steps(self, steps):
        pass

    # temporary function
    def contact_with_floor(self):
        if self.rect.bottom >= 700:
            self.floor_under_legs_status = True

    def update(self):
        self.player_input()
        self.gravity_function()
        self.contact_with_floor()
