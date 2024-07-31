import unittest
import pygame
from engine import Engine
from steps_lib import FloorSnowbiom, StepSnowbiom
from player import Player
from constant_var import SCREEN_WIDTH, SCREEN_HEIGHT

class EngineTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player_group = pygame.sprite.GroupSingle()
        self.steps_group = pygame.sprite.Group()
        
        self.player = Player()
        self.player_group.add(self.player)
        
        self.engine = Engine(self.player_group, self.steps_group, self.screen)

    def test_is_contact_with_step(self):
        step = StepSnowbiom(300, 1)
        step.rect.top = 300
        self.player.rect.bottom = 310
        self.player.rect.centerx = step.rect.centerx
        self.player.y_speed = 1
        
        self.assertTrue(self.engine._is_contact_with_step(step))

    def test_check_player_can_do_more_combo(self):
        self.engine.combo_start_time = pygame.time.get_ticks() - 1000
        self.engine._check_player_can_do_more_combo()
        self.assertTrue(self.engine.can_do_more_combo)
        
        self.engine.combo_start_time = pygame.time.get_ticks() - 4000
        self.engine._check_player_can_do_more_combo()
        self.assertFalse(self.engine.can_do_more_combo)

    def test_get_step_under_player(self):
        step = StepSnowbiom(300, 1)
        step.rect.top = 300
        self.steps_group.add(step)
        self.player.rect.bottom = 310
        self.player.rect.centerx = step.rect.centerx
        self.player.y_speed = 1
        
        self.assertEqual(self.engine._get_step_under_player(), step)

    def test_update_score_and_level(self):
        self.engine.level = 5
        self.engine.score = 100
        self.engine._update_score_and_level(3)
        self.assertEqual(self.engine.level, 8)
        self.assertEqual(self.engine.score, 130)

    def test_display_text(self):
        self.engine._display_text('Test', (100, 100))
        # Cannot easily test the blitting, but no exceptions should be raised.

    def test_spawning_steps(self):
        initial_length = len(self.engine.list_of_steps)
        self.engine.spawning_steps()
        self.assertGreater(len(self.engine.list_of_steps), initial_length)

    def test_adjust_steps(self):
        self.player.rect.top = 50
        self.player.y_speed = -5
        initial_step_rect_top = self.engine.my_steps.sprites()[0].rect.top
        self.engine.adjust_steps()
        self.assertNotEqual(self.engine.my_steps.sprites()[0].rect.top, initial_step_rect_top)

    def test_contact_with_steps(self):
        step = StepSnowbiom(300, 1)
        step.rect.top = 300
        self.steps_group.add(step)
        self.player.rect.bottom = 310
        self.player.rect.centerx = step.rect.centerx
        self.player.y_speed = 1
        
        self.engine.contact_with_steps()
        self.assertTrue(self.player.can_jump)
        self.assertEqual(self.player.y_speed, 0)
        
    def test_time_destroying_steps(self):
        self.player.current_height = 100
        step = StepSnowbiom(300, 1)
        step.step_height = 50
        self.steps_group.add(step)
        
        self.engine.time_destroying_steps()
        self.assertTrue(step.destruction)

    def test_update_result(self):
        step = StepSnowbiom(300, 3)
        step.rect.top = 300
        self.steps_group.add(step)
        self.player.rect.bottom = 310
        self.player.rect.centerx = step.rect.centerx
        self.player.y_speed = 1
        
        self.engine.level = 1
        self.engine._get_step_under_player = lambda: step  # Mock the method
        self.engine.update_result()
        self.assertEqual(self.engine.level, 3)
        self.assertEqual(self.engine.score, 20)

    def test_reset(self):
        self.engine.level = 10
        self.engine.score = 200
        self.engine.reset()
        self.assertEqual(self.engine.level, 0)
        self.assertEqual(self.engine.score, 0)
        self.assertEqual(len(self.engine.my_steps), 1)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
