import pygame
from steps_lib import StepSnowbiom, StepLavabiom, StepJunglebiom, FloorSnowbiom

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

    def spawning_steps(self):
        new_steps_list = []
        for step in self.list_of_steps:
            if step.absolute_height < self.my_player.sprite.max_height + 1000:
                self.my_steps.add(step)
                if step.number < 10:
                    new_step = StepSnowbiom(step.absolute_height + 1000, step.number + 5)
                elif step.number < 20:
                    new_step = StepJunglebiom(step.absolute_height + 1000, step.number + 5)
                else:
                    new_step = StepLavabiom(step.absolute_height + 1000, step.number + 5)
                new_steps_list.append(new_step)
        self.list_of_steps += new_steps_list
        self.list_of_steps = self.list_of_steps[len(new_steps_list):]

    def adjust_steps(self):
        if self.my_player.sprite.rect.bottom > 200:
            for step in self.my_steps:
                step.rect.top = 800 - step.absolute_height + self.my_player.sprite.current_height
        else:
            for step in self.my_steps:
                step.absolute_height += self.my_player.sprite.y_speed
                step.rect.top = 800 - step.absolute_height + self.my_player.sprite.current_height
            for step in self.list_of_steps:
                step.absolute_height += self.my_player.sprite.y_speed

    def check_result(self):
        for step in self.my_steps:
            if (step.rect.top == self.my_player.sprite.rect.bottom and self.my_player.sprite.y_speed == 0
                    and step.rect.right >= self.my_player.sprite.rect.centerx >= step.rect.left):  # czy nie naliczy obok dla y =0 zlego maxa?
                self.level = max(self.level, step.number)
                self.score = max(self.score, step.number)

    def contact_with_steps(self):
        flag_1 = False
        for step in self.my_steps:
            if (step.rect.top - 10 <= self.my_player.sprite.rect.bottom <= step.rect.top + 10 and
                    step.rect.left <= self.my_player.sprite.rect.centerx <= step.rect.right and
                    self.my_player.sprite.y_speed >= 0):
                self.my_player.sprite.can_jump = True
                self.my_player.sprite.super_jump = False
                self.my_player.sprite.rect.bottom = step.rect.top
                self.my_player.sprite.y_speed = 0
                flag_1 = True
                #step.destruction = True
        if not flag_1:
            self.my_player.sprite.can_jump = False

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

    def update(self):
        self.spawning_steps()
        self.adjust_steps()
        self.contact_with_steps()
        self.check_result()

        self.my_player.draw(self.main_screen)
        self.my_player.update()

        self.my_steps.draw(self.main_screen)
        self.my_steps.update()
