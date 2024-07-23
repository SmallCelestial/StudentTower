import pygame
from steps_lib import StepSnowbiom, StepLavabiom, StepJunglebiom, FloorSnowbiom


class Engine:
    def __init__(self, player: pygame.sprite.GroupSingle, steps: pygame.sprite.Group, screen):
        super().__init__()
        self.my_player = player  # this is GroupSingle
        self.my_steps = steps  # this is Group
        self.main_screen = screen

        self.list_of_steps = [[400, 1, StepSnowbiom(400, 1)],
                              [600, 1, StepSnowbiom(600, 2)],
                              [800, 1, StepSnowbiom(800, 3)],
                              [1000, 1, StepSnowbiom(1000, 4)],
                              [1200, 1, StepSnowbiom(1200, 5)]]

        self.my_steps.add(FloorSnowbiom(100, 0))

        self.level = 0
        self.max_combo = 0
        self.score = 0

    def spawning_steps(self):
        new_steps_list = []
        for step in self.list_of_steps:
            if step[0] < self.my_player.sprite.current_height + 1000:
                self.my_steps.add(step[2])
                ####
                if step[0] + 1000 < 2000:
                    new_step = [step[0] + 1000, 1, StepSnowbiom(step[0] + 1000, step[2].number + 5)]
                elif step[0] + 1000 < 3000:
                    new_step = [step[0] + 1000, 2, StepJunglebiom(step[0] + 1000, step[2].number + 5)]
                else:
                    new_step = [step[0] + 1000, 3, StepLavabiom(step[0] + 1000, step[2].number + 5)]
                new_steps_list.append(new_step)
                ####
        self.list_of_steps += new_steps_list
        self.list_of_steps = self.list_of_steps[len(new_steps_list):]

    def display_steps(self):
        if self.my_player.sprite.rect.top > 100:
            for step in self.my_steps:
                step.rect.top = 800 - step.height + self.my_player.sprite.current_height
        else:
            for step in self.my_steps:
                step.height += self.my_player.sprite.y_speed
                step.rect.top = 800 - step.height + self.my_player.sprite.current_height
            for step in self.list_of_steps:
                step[0] += self.my_player.sprite.y_speed
                step[2].height = step[0]

    def check_result(self):
        for step in self.my_steps:
            if step.rect.top == self.my_player.sprite.rect.bottom and self.my_player.sprite.y_speed == 0:
                self.level = max(self.level, step.number)
                self.score = max(self.score, step.number)
                print(step.number)

    def contact_with_steps(self):
        flag_1 = False
        for step in self.my_steps:
            if (step.rect.top - 4 <= self.my_player.sprite.rect.bottom <= step.rect.top + 10 and
                    step.rect.left <= self.my_player.sprite.rect.centerx <= step.rect.right and
                    self.my_player.sprite.y_speed >= 0):
                self.my_player.sprite.can_jump = True
                self.my_player.sprite.rect.bottom = step.rect.top
                self.my_player.sprite.y_speed = 0
                flag_1 = True
                step.destruction = True  # destruction when collision for now
        if not flag_1:
            self.my_player.sprite.can_jump = False

    def reset(self):
        self.list_of_steps = [[400, 1, StepSnowbiom(400, 1)],
                              [600, 1, StepSnowbiom(600, 2)],
                              [800, 1, StepSnowbiom(800, 3)],
                              [1000, 1, StepSnowbiom(1000, 4)],
                              [1200, 1, StepSnowbiom(1200, 5)]]
        self.my_steps.empty()
        self.my_steps.add(FloorSnowbiom(100, 0))
        self.my_player.sprite.reset()
        self.level = 0
        self.max_combo = 0
        self.score = 0
    
    def update(self):
        self.spawning_steps()
        self.display_steps()
        # self.display_player()
        self.contact_with_steps()
        self.check_result()

        self.my_player.draw(self.main_screen)
        self.my_player.update()

        self.my_steps.draw(self.main_screen)
        self.my_steps.update()
