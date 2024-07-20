import pygame
from random import randint


class Intro():
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.main_screen = screen
        self.image = pygame.image.load('resources/backgrounds/handpaintedwall2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (1000, 800))

        self.rect = self.image.get_rect(center=(500, 400))
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

    def update(self):
        self.draw()
        self.check_buttons()


class RotatePlayer(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('resources/PLayer/player_stand.png').convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, (0.75, 0.75))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(775, 500))
        self.counter = 0
        self.angle = 0

    def rotate_player(self):
        self.counter += 1
        if self.counter % 10 == 0:
            self.angle = (self.angle + 60) % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=(775, 500))

    def update(self):
        self.rotate_player()


class Floor(pygame.sprite.Sprite):

    def __init__(self, leftbottom):
        super().__init__()
        self.image = pygame.image.load('resources/floors/step_snowbiom_0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 30))
        self.rect = self.image.get_rect(bottomleft=leftbottom)

    def move_up(self):
        self.rect.centery -= 1

    def update(self):
        self.move_up()


class AllFloors:

    def __init__(self):
        self.floors_group = pygame.sprite.Group()
        height = 1000
        for _ in range(8):
            left = randint(600, 800)
            self.floors_group.add(Floor((left, height)))
            height -= 200

    def check_steps(self):
        to_add = []
        for step in self.floors_group:
            if step.rect.centery <= -600:
                self.floors_group.remove(step)
                left = randint(600, 800)
                to_add.append(Floor((left, 1000)))
        self.floors_group.add(to_add)

    def update(self):
        self.check_steps()
        self.floors_group.update()

    def draw(self, screen):
        self.floors_group.draw(screen)


def display_text(text, font, topleft, image):
    text_surface = font.render(text, True, "Brown")
    text_rect = text_surface.get_rect(topleft=topleft)
    image.blit(text_surface, text_rect)


class Outro:

    def __init__(self, screen, level=0, max_combo=0, score=0):

        self.level = level
        self.max_combo = max_combo
        self.score = score

        self.main_screen = screen
        self.image = pygame.image.load('resources/backgrounds/background.xcf').convert_alpha()
        self.image = pygame.transform.scale(self.image, (1000, 800))
        self.rect = self.image.get_rect(center=(500, 400))

        # falling player
        self.rotate_player_group = pygame.sprite.GroupSingle()
        self.rotate_player_group.add(RotatePlayer())

        # Images are just temporary
        self.play_image = pygame.image.load('resources/backgrounds/PlayButtonHighlight.png').convert_alpha()
        self.play_image = pygame.transform.scale(self.play_image, (300, 150))
        self.play_image_rect = self.play_image.get_rect(bottomleft=(150, 600))
        self.image.blit(self.play_image, self.play_image_rect)

        self.menu_image = pygame.image.load('resources/backgrounds/PlayButtonHighlight.png').convert_alpha()
        self.menu_image = pygame.transform.scale(self.menu_image, (300, 150))
        self.menu_image_rect = self.menu_image.get_rect(bottomleft=(150, 700))
        self.image.blit(self.menu_image, self.menu_image_rect)

        self.exit_image = pygame.image.load('resources/backgrounds/PlayButtonHighlight.png').convert_alpha()
        self.exit_image = pygame.transform.scale(self.exit_image, (300, 150))
        self.exit_image_rect = self.exit_image.get_rect(bottomleft=(150, 800))
        self.image.blit(self.exit_image, self.exit_image_rect)

        # Floors
        self.floors_group = AllFloors()

        # Text
        font = pygame.font.SysFont("Comic Sans MS", 75)
        display_text("GAME OVER", font, (130, 5), self.image)

        # Result
        font = pygame.font.SysFont("Comic Sans MS", 40)
        display_text("Level: {}".format(self.level), font, (180, 150), self.image)
        display_text("Max combo: {}".format(self.max_combo), font, (180, 200), self.image)
        display_text("Total score: {}".format(self.score), font, (180, 250), self.image)
        display_text("Best score: {}".format(9999), font, (180, 300), self.image)

        self.status = "outro"

    def check_buttons(self):
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_state[0] == 1:
            if self.play_image_rect.collidepoint(mouse_pos):
                self.status = "game_on"
            elif self.menu_image_rect.collidepoint(mouse_pos):
                self.status = "intro"
            elif self.exit_image_rect.collidepoint(mouse_pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        self.main_screen.blit(self.image, self.rect)

        self.rotate_player_group.update()
        self.rotate_player_group.draw(self.main_screen)

        self.floors_group.update()
        self.floors_group.draw(self.main_screen)

        self.check_buttons()
