import pygame
from steps_lib import FloorSnowbiom, StepSnowbiom, StepSnowbiom250, StepSnowbiom200
from steps_lib import StepLavabiom, StepJunglebiom
import math
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class Engine:
    def __init__(self, player: pygame.sprite.GroupSingle, steps: pygame.sprite.Group, screen):
        super().__init__()
        self.my_player = player  # this is GroupSingle
        self.my_steps = steps  # this is Group
        self.main_screen = screen

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
        self.start_time = pygame.time.get_ticks()
        self.combo_timer = 0
        self.combo_start_time = 0

    def _is_contact_with_step(self, step):
        if (step.rect.top - 10 <= self.my_player.sprite.rect.bottom <= step.rect.top + 10 and
                step.rect.left <= self.my_player.sprite.rect.centerx <= step.rect.right and
                self.my_player.sprite.y_speed >= 0):
            return True
        return False

    def _check_player_can_do_more_combo(self):
        self.combo_timer = 3000 - (pygame.time.get_ticks() - self.combo_start_time)
        if self.combo_start_time == 0 or self.combo_timer > 0:
            self.can_do_more_combo = True
        else:
            self.can_do_more_combo = False

    def _get_step_under_player(self):
        for step in self.my_steps:
            if self._is_contact_with_step(step):
                return step
        return None

    def _update_score_and_level(self, level_difference):
        if level_difference > 0:
            self.score += level_difference * 10
            self.level += level_difference

    def _display_text(self, text, top_left):
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
                    new_step = StepJunglebiom(step.step_height + 1000, step.step_number + 5)
                else:
                    new_step = StepLavabiom(step.step_height + 1000, step.step_number + 5)
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
                # step.destruction = True
        if not flag_1:
            self.my_player.sprite.can_jump = False

    def time_destroying_steps(self):
        self.timer_for_steps = int((pygame.time.get_ticks() - self.start_time) / 25)
        # factor/divisor regulates how fast x-argument in log function
        # while base of logarithm regulates estimated max_multiplier, y in log function
        self.timer_for_steps_multiplier = math.log(3 + (pygame.time.get_ticks() - self.start_time) / 20000, 3)
        for step in self.my_steps:
            if step.step_height < max(self.my_player.sprite.current_height - 100,
                                      int(self.timer_for_steps * self.timer_for_steps_multiplier)):
                step.destruction = True
        # print(f"{self.timer_for_steps_multiplier}_{self.timer_for_steps}")

    def update_result(self):
        self._check_player_can_do_more_combo()
        step_under_player = self._get_step_under_player()

        if not step_under_player:
            return

        level_difference = step_under_player.step_number - self.level
        self._update_score_and_level(level_difference)

        if self.can_do_more_combo and level_difference > 1:
            self.current_combo += level_difference
            self.combo_start_time = pygame.time.get_ticks()
        elif not self.can_do_more_combo or level_difference == 1:
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
        self.list_of_steps = [StepSnowbiom(300, 1),
                              StepSnowbiom(500, 2),
                              StepSnowbiom(700, 3),
                              StepSnowbiom(900, 4),
                              StepSnowbiom(1100, 5)]
        self.my_steps.empty()
        self.my_steps.add(FloorSnowbiom(100, 0))
        self.my_player.sprite.reset()
        self.level = 0
        self.max_combo = 0
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.current_combo = 0
        self.can_do_more_combo = True
        self.start_time = pygame.time.get_ticks()
        self.combo_timer = 0
        self.combo_start_time = 0

    def update(self):
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
