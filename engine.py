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

        self.list_of_steps = [[100, "to_spawn", Floor_snowbiom(100)], [400, "to_spawn", Step_snowbiom(400)],
                              [600, "to_spawn", Step_snowbiom(600)], [800, "to_spawn", Step_snowbiom(800)],
                              [1000, "to_spawn", Step_snowbiom(1000)], [1200, "to_spawn", Step_snowbiom(1200)],
                              [1400, "to_spawn", Step_snowbiom(1400)], [1600, "to_spawn", Step_snowbiom(1600)]]

    def spawning_steps(self):
        for step in self.list_of_steps:
            if step[0] < self.my_player.sprite.current_height + 1000 and step[1] == "to_spawn":
                step[1] = "spawned"
                falling_floors_group.add(step[2])

    def display_steps(self):
        for step in self.my_steps:
            step.rect.top = 800 - step.height + self.my_player.sprite.current_height

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
        self.contact_with_steps()

        self.my_player.draw(main_screen)
        self.my_player.update()

        self.my_steps.draw(main_screen)
        self.my_steps.update()
