from engine import Engine
import pygame
from screens import Intro, Outro
from time import sleep
from player import Player
from database.database_handler import ScoreDatabase
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()
main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Student_Tower")
main_clock = pygame.time.Clock()
game_status = "intro"

falling_floors_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

intro = Intro(main_screen)
outro = Outro(main_screen)
scores_db = ScoreDatabase('data.sqlite')
main_engine = Engine(player_group, falling_floors_group, main_screen)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif game_status == "game_on" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_status = "outro"

    if game_status == "game_on":
        main_engine.update()

        if not main_engine.my_player.sprite.is_alive:
            game_status = "outro"
            scores_db.add_score(main_engine.score)
            outro.max_score = scores_db.get_max_score()
    elif game_status == "intro":
        intro.update()
        if intro.play_button:
            game_status = "game_on"
            intro.play_button = False
    elif game_status == "outro":

        outro.score = main_engine.score
        outro.level = main_engine.level
        outro.max_combo = main_engine.max_combo
        outro.update()
        if outro.status == "game_on":
            sleep(0.2)
            main_engine.reset()
            game_status = "game_on"
            outro.status = "outro"
        elif outro.status == "intro":
            sleep(0.2)
            main_engine.reset()
            game_status = "intro"
            outro.status = "outro"

    pygame.display.update()
    main_clock.tick(60)
