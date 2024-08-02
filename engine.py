import pygame
from steps_lib import (FloorSnowbiom, StepSnowbiom, StepSnowbiom250, StepSnowbiom200,
                       StepJunglebiom, StepJunglebiom250, StepJunglebiom200,
                       StepLavabiom, StepLavabiom250, StepLavabiom200,
                       StepTemplate)
import math
import random


class Engine:
    """
    Engine class is responsible for interaction of player, steps, screens classes.

    Attributes:
    -----------
    my_player : pygame.sprite.GroupSingle
        it contains player object in Groupsingle, which is created in main.py file, but given in
        engine-class constructor.
    my_steps : pygame.sprite.Group
        it contains steps object in Group, which currently exists and are shown on screen, this group
        is created in main.py file, but is given in engine class-constructor.
    main_screen : pygame.display
        it contains instance of main screen, which is created in main.py file, but is provided in
        eingine-class constructor.
    start_background : pygame.image
        Texture og backgound shown during gameplay
    list_of_steps : list
        it contains steps with their spawnheight and their index numeration from the bottom, when 
        spawning_steps() fuction decides that certain steps should be spawned it will remove it form
        the list and add it to my_steps group (for it to be displayed)
    level : int
        Represents the maximum step number on which the player has stood during the game.
    max_combo : int
        Represents the maximum combo achieved by the player in the current game session.
    score : int
        Represents the player's current score.
    current_combo : int
        Represents the current combo count.
    font : pygame.font
        default font for displaying mid-game information (like combo score, current level etc.)
    start_time : pygame.time
        it holds the tick number when certain game-run started. The length of game-run is 
        subtraction of current tick number (updated every second during gamplay) and start_time tick.
    combo_timer : int
        The amount of time remaining, in milliseconds, to continue the current combo.
    combo_start_time : int
        The tick number when the current combo started.
    
    Methods:
    -------
    __init__() :
        Initialises engine object with player_group, falling_floors_group and main_screen.
    _is_contact_with_step() : bool
        it checks whether player stays on certain step or not and return adequate bool value
    _check_player_can_do_more_combo() : bool
        it checks whether player can cantinue the current combo or not and return adequate bool value
    _get_step_under_player() : pygame.sprite.Group.sprites()[]
        it returns the step-object player currently stays on (and None if player stays on none).
    _update_score_and_level() :
        it updates score and level of current game-run
    _display_text() :
        it displays given text on main_screen with font mentioned in attributes
    spawning_steps():
        This method works on list_of_steps. It decides when stair should be transplanted from 
        list_of_steps to my_steps group by comparing the height on which steps is placed and height on 
        which player currently is. Also, when one step is removed from list_of_steps, new step with 
        greater spawn height is added at the end of the list. Which step is added depends on its 
        step_number. For example, when step which is about to be added to list_of_steps should have 
        step_number between 20 and 39,  it will result in adding junglebiom step at the end of the
        list_of_steps. This creates instance of junglebiom from step nr 20 to step nr 39.
    adjust_steps():
        This method is responsible for how player and stairs are displayed. When player gets to the 
        upper part of screen, instead of moving him even higher, we move  steps downwards
        prioportionally more. Thanks to it player, player stays on certain high of a screen without
        messing the relation of distance between player and steps surrounding him.
    contact_with_steps():
    time_destroying_steps():
    update_result():
       Updates the game result based on the current state, including the score and level, at the moment the game is being updated.
    display_result():
    display_combo_timer():
    display_combo():
    reset():
    update():
    """
    def __init__(self, player: pygame.sprite.GroupSingle, steps: pygame.sprite.Group, screen):
        super().__init__()
        self.my_player = player
        self.my_steps = steps
        self.main_screen = screen
        self.start_background = pygame.image.load('resources/backgrounds/background.png').convert_alpha()

        self.list_of_steps = None
        self.level = None
        self.max_combo = None
        self.score = None
        self.current_combo = None
        self.font = None
        self.start_time = None
        self.combo_timer = None
        self.combo_start_time = None

        self._setup_game_parameters()

    def _setup_game_parameters(self):
        self.list_of_steps = [StepSnowbiom(300, 1),
                              StepSnowbiom(500, 2),
                              StepSnowbiom(700, 3),
                              StepSnowbiom(900, 4),
                              StepSnowbiom(1100, 5)]

        self.my_steps.add(FloorSnowbiom(100, 0))

        self.level = 0
        self.max_combo = 0
        self.score = 0

        self.current_combo = 0
        self.can_do_more_combo = True
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.start_time = 0
        self.combo_timer = 0
        self.combo_start_time = 0

    def _is_contact_with_step(self, step: StepTemplate) -> bool:
        if (step.rect.top - 10 <= self.my_player.sprite.rect.bottom <= step.rect.top + 10 and
                step.rect.left <= self.my_player.sprite.rect.centerx <= step.rect.right and
                self.my_player.sprite.y_speed >= 0):
            return True
        return False

    def _check_player_can_do_more_combo(self):
        self.combo_timer = 3000 - (pygame.time.get_ticks() - self.combo_start_time)
        if self.combo_start_time == 0 or self.combo_timer > 0:
            self.my_player.sprite.can_do_more_combo = True
        else:
            self.my_player.sprite.can_do_more_combo = False

    def _get_step_under_player(self) -> StepTemplate | None:
        for step in self.my_steps:
            if self._is_contact_with_step(step):
                return step
        return None

    def _update_score_and_level(self, level_difference: int):
        if level_difference > 0:
            self.score += level_difference * 10
            self.level += level_difference

    def _display_text(self, text: str, top_left: tuple[int, int]):
        text_surface = self.font.render(text, True, "Brown")
        text_rect = text_surface.get_rect(topleft=top_left)
        self.main_screen.blit(text_surface, text_rect)

    def spawning_steps(self):
        new_steps_list = []
        for step in self.list_of_steps:
            if step.step_height < self.my_player.sprite.max_height + 1000:
                self.my_steps.add(step)
                if step.step_number < 20:
                    new_step = random.choice(
                        [StepSnowbiom(step.step_height + 1000, step.step_number + 5),
                         StepSnowbiom250(step.step_height + 1000, step.step_number + 5),
                         StepSnowbiom200(step.step_height + 1000, step.step_number + 5)])
                elif step.step_number < 40:
                    new_step = random.choice(
                        [StepJunglebiom(step.step_height + 1000, step.step_number + 5),
                         StepJunglebiom250(step.step_height + 1000, step.step_number + 5),
                         StepJunglebiom200(step.step_height + 1000, step.step_number + 5)])
                else:
                    new_step = random.choice(
                        [StepLavabiom(step.step_height + 1000, step.step_number + 5),
                         StepLavabiom250(step.step_height + 1000, step.step_number + 5),
                         StepLavabiom200(step.step_height + 1000, step.step_number + 5)])
                new_steps_list.append(new_step)
        self.list_of_steps += new_steps_list
        self.list_of_steps = self.list_of_steps[len(new_steps_list):]

    def adjust_steps(self):
        if self.my_player.sprite.rect.top > 120:
            for step in self.my_steps:
                step.rect.top = 800 - step.step_height + self.my_player.sprite.current_height
        else:
            for step in self.my_steps:
                step.step_height += self.my_player.sprite.y_speed
                step.rect.top = 800 - step.step_height + self.my_player.sprite.current_height
            for step in self.list_of_steps:
                step.step_height += self.my_player.sprite.y_speed

    def contact_with_steps(self):
        flag_1 = False
        for step in self.my_steps:
            if self._is_contact_with_step(step):
                self.my_player.sprite.can_jump = True
                self.my_player.sprite.super_jump = False
                self.my_player.sprite.rect.bottom = step.rect.top
                self.my_player.sprite.y_speed = 0
                flag_1 = True
                if self.my_player.sprite.current_height > 500:
                    step.destruction = True
        if not flag_1:
            self.my_player.sprite.can_jump = False

    def time_destroying_steps(self): 
        if self.my_player.sprite.max_height <= 200:
            self.start_time = pygame.time.get_ticks()
        timer_for_steps = (pygame.time.get_ticks() - self.start_time) // 25

        timer_for_steps_multiplier = math.log(3 + (pygame.time.get_ticks() - self.start_time) / 10000, 3)
        for step in self.my_steps:
            if step.step_height < max(self.my_player.sprite.current_height - 100,
                                      int(timer_for_steps * timer_for_steps_multiplier)):
                step.destruction = True

    def update_result(self):
        self._check_player_can_do_more_combo()
        step_under_player = self._get_step_under_player()

        if not step_under_player:
            return

        level_difference = step_under_player.step_number - self.level
        self._update_score_and_level(level_difference)

        if self.my_player.sprite.can_do_more_combo and level_difference > 1:
            self.current_combo += level_difference
            self.combo_start_time = pygame.time.get_ticks()
        elif not self.my_player.sprite.can_do_more_combo or level_difference == 1 or level_difference < 0:
            self.score += self.current_combo ** 2 * 5
            self.max_combo = max(self.max_combo, self.current_combo)
            self.current_combo = 0
            self.combo_start_time = 0

    def display_result(self):
        self._display_text(str(self.score), (100, 0))

    def display_combo_timer(self):
        if self.combo_timer > 0 and self.level != 0:
            self._display_text(str(self.combo_timer), (820, 0))

    def display_combo(self):
        if self.current_combo > 0:
            self._display_text(str(self.current_combo), (850, 50))

    def reset(self):
        self.my_steps.empty()
        self.my_player.sprite.reset()
        self._setup_game_parameters()

    def update(self):
        self.main_screen.blit(self.start_background, (0, 0))
        self.spawning_steps()
        self.adjust_steps()
        self.contact_with_steps()
        self.time_destroying_steps()
        self.update_result()
        self.display_combo_timer()
        self.display_combo()

        self.my_player.draw(self.main_screen)
        self.my_player.update()

        self.my_steps.draw(self.main_screen)
        self.my_steps.update()

        self.display_result()
