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
    def __init__(self, player, steps):
        super().__init__()
        self.my_player = player  # this is GroupSingle
        self.my_steps = steps  # this is Group

        self.list_of_steps = [[400,Step_snowbiom(400), 0],
                              [600,Step_snowbiom(600), 1], [800,Step_snowbiom(800), 2],
                              [1000,Step_snowbiom(1000), 3], [1200,Step_snowbiom(1200), 4],
                              [1400,Step_snowbiom(1400), 5], [1600,Step_snowbiom(1600), 6]]
        self.my_steps.add(Floor_snowbiom(100))

    def spawning_steps(self):
        new_steps_list = []
        for step in self.list_of_steps:
            if step[0] < self.my_player.sprite.current_height + 1000:
                self.my_steps.add(step[1])
                if step[0] + 1400 < 3000:
                    new_step = [step[0] + 1400,Step_snowbiom(step[0] + 1400), step[2] + 7]
                else:
                    new_step = [step[0] + 1400,Step_junglebiom(step[0] + 1400), step[2] + 7]
                new_steps_list.append(new_step)
        self.list_of_steps += new_steps_list
        self.list_of_steps = self.list_of_steps[len(new_steps_list):]

    def display_steps(self):
        if self.my_player.sprite.rect.top > 100:
            for step in falling_floors_group:
                step.rect.top = 800 - step.height + self.my_player.sprite.current_height
        else:
            for step in falling_floors_group:
                print(step.biom_id)
                step.height += self.my_player.sprite.y_speed
                step.rect.top = 800 - step.height + self.my_player.sprite.current_height
            for step in self.list_of_steps:
                step[0] += self.my_player.sprite.y_speed
                step[1] = Step_snowbiom(step[0])

    # def display_player(self):
    #     # Constrain player position
    #     if self.my_player.sprite.rect.top < 100:
    #         self.my_player.sprite.rect.top = 100
    #     if self.my_player.sprite.rect.bottom > 700:
    #         self.my_player.sprite.rect.bottom = 700

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
        if not flag_1:
            self.my_player.sprite.can_jump = False
    
    def update(self):
        self.spawning_steps()
        self.display_steps()
        # self.display_player()
        self.contact_with_steps()

        self.my_player.draw(main_screen)
        self.my_player.update()

        self.my_steps.draw(main_screen)
        self.my_steps.update()
