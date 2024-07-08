import pygame

pygame.init()
main_screen=pygame.display.set_mode((800,400)) #width,height
pygame.display.set_caption("Pixel_Runner")

main_clock=pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
       
    
    pygame.display.update()
    main_clock.tick(60) #maximum frameratxxxx
