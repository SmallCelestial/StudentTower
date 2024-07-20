from player import *

WIDTH = 1000
HEIGHT = 800

# SCREEN initialization
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Student_Tower")

# GROUPS
falling_floors_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
player_group.add(Player()) 


class Engine:
    def __init__(self, player: pygame.sprite.GroupSingle, steps: pygame.sprite.Group):
        super().__init__()
        self.my_player = player  # this is GroupSingle
        self.my_steps = steps  # this is Group

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

    # def spawning_steps(self):
    #     new_steps_list = []
    #     for step in self.my_steps:
    #         if step.height < self.my_player.sprite.current_height + 1000:
    #             ####
    #             if step.height + 1000 < 2000:
    #                 new_step = StepSnowbiom(step.height + 1000, step.number + 5)
    #             elif step.height + 1000 < 3000:
    #                 new_step = StepJunglebiom(step.height + 1000, step.number + 5)
    #             else:
    #                 new_step = StepLavabiom(step.height + 1000, step.number + 5)
    #             new_steps_list.append(new_step)
    #             self.my_steps.remove(step)
    #             ####
    #     self.my_steps.add(new_steps_list)
    #     print([step[0] for step in self.list_of_steps])

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
                ####
                if step[1] == 1:
                    print(step[2].number)
                    step[2] = StepSnowbiom(step[0], step[2].number + 5)
                elif step[1] == 2:
                    print(step[2].number)
                    step[2] = StepJunglebiom(step[0], step[2].number + 5)
                elif step[1] == 3:
                    print(step[2].number)
                    step[2] = StepLavabiom(step[0], step[2].number + 5)
            #     ####

    # def display_player(self):
    #     # Constrain player position
    #     if self.my_player.sprite.rect.top < 100:
    #         self.my_player.sprite.rect.top = 100
    #     if self.my_player.sprite.rect.bottom > 700:
    #         self.my_player.sprite.rect.bottom = 700

    def check_result(self):
        for step in self.my_steps:
            if step.rect.top == self.my_player.sprite.rect.bottom and self.my_player.sprite.y_speed == 0:
                self.level = max(self.level, step.number)
                self.score = max(self.score, step.number)
                print(step.number)

    def contact_with_steps(self):
        flag_1 = False
        for step in self.my_steps:
            if (step.rect.top - 2 <= self.my_player.sprite.rect.bottom <= step.rect.top + 10 and
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
        falling_floors_group.empty()
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

        self.my_player.draw(main_screen)
        self.my_player.update()

        self.my_steps.draw(main_screen)
        self.my_steps.update()
