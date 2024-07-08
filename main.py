import pygame

pygame.init()
main_screen=pygame.display.set_mode((800,400)) #width,height
pygame.display.set_caption("Pixel_Runner")

#CLASSES
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk=pygame.image.load("resources/Player/player_stand.png").convert_alpha()

        self.image= self.player_walk #jakbys zmienial to napisz
        self.rect=self.image.get_rect(midbottom=(100,100)) #jakbys zmienial to napisz


#GLOBAL VARIABLES
main_clock=pygame.time.Clock()
new_Variable=100
game_status="game_on" #intro, game_on, outro

sky_surface=pygame.image.load('resources/backgrounds/Sky.png').convert_alpha()
floor_surface=pygame.image.load('resources/backgrounds/ground.png').convert_alpha()

#GROUPS
player=pygame.sprite.GroupSingle()
player.add(Player())


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    if game_status == "game_on":
        
        main_screen.blit(sky_surface,(0,0))
        main_screen.blit(floor_surface,(0,300))

        player.draw(main_screen)
        player.update()
       

    pygame.display.update()
    main_clock.tick(60) #maximum frameratxxxx
