import pygame

pygame.init()
main_screen=pygame.display.set_mode((1000,800)) #width,height
pygame.display.set_caption("Student_Tower")

main_clock=pygame.time.Clock()
#GLOBAL VARIABLES
game_status="game_on" # intro, game_on, outro


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    
    if game_status == "game_on":
        pass
        
    
    pygame.display.update()
    main_clock.tick(60) #maximum framerate