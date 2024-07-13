import pygame
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


class Engine():
    def __init__(self, player, steps):
        super().__init__()
        self.my_player = player # this is GroupSingle
        self.my_steps = steps # this is Group

        ##self.nr_of_steps_spawned=5
        self.list_of_steps = [[100,"to_spawn",Floor_snowbiom(100)], [400,"to_spawn",Step_snowbiom(400)],
                            [600,"to_spawn",Step_snowbiom(600)], [800,"to_spawn",Step_snowbiom(800)],
                            [1000,"to_spawn",Step_snowbiom(1000)], [1200,"to_spawn",Step_snowbiom(1200)],
                            [1400,"to_spawn",Step_snowbiom(1400)], [1600,"to_spawn",Step_snowbiom(1600)]]

   ## def spawning_steps(self, player_gr): 
   ##    player = player_gr.sprite
   ##    for iter in range(0,self.nr_of_steps_spawned):
   ##        if self.list_of_steps[iter][0] < player.current_height + 1000 and self.list_of_steps[iter][1] == "to_spawn":
   ##            self.list_of_steps[iter][1] = "spawned"
   ##            falling_floors_group.add(self.list_of_steps[iter][2])
   ##            #self.nr_of_steps_spawned += 1
    def spawning_steps(self, player_gr):
        player = player_gr.sprite
        for step in self.list_of_steps:
            if step[0] < player.current_height + 1000 and step[1] == "to_spawn":
                step[1] = "spawned"
                falling_floors_group.add(step[2])

    def display_steps(self, player_gr, steps):
        player = player_gr.sprite
        for step in steps:
            step.rect.top = 800 - step.height + player.current_height 

    def contact_with_steps(self, player_gr, steps):
        player = player_gr.sprite
        flag_1 = False
        for step in steps:
            if (step.rect.top + 5 >= player.rect.bottom >= step.rect.top - 5 and
                    step.topLeft[0] <= player.rect.centerx <= step.topRight[0] and
                    player.y_speed >= 0):
                player.can_jump = True
                player.rect.bottom = step.rect.top
                player.y_speed = 0
                flag_1 = True
        if not flag_1:
            player.can_jump = False
    
    def update(self):
        self.spawning_steps(self.my_player)
        self.display_steps(self.my_player,  self.my_steps)
        self.contact_with_steps(self.my_player, self.my_steps)

        self.my_player.draw(main_screen)
        self.my_player.update()

        self.my_steps.draw(main_screen)
        self.my_steps.update()


