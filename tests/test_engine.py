import unittest
from unittest.mock import patch, MagicMock

import pygame
import os

from engine import Engine
from steps_lib import FloorSnowbiom, StepSnowbiom
from player import Player


class EngineTestCase(unittest.TestCase):

    original_directory = None

    @classmethod
    def setUpClass(cls):
        cls.original_directory = os.getcwd()
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.original_directory)

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1, 1))
        self.player_group = pygame.sprite.GroupSingle()
        self.steps_group = pygame.sprite.Group()

        self.player = Player()
        self.player_group.add(self.player)

        self.engine = Engine(self.player_group, self.steps_group, self.screen)

    def tearDown(self):
        pygame.quit()

    def check_parameters(self):
        self.assertEqual(5, len(self.engine.list_of_steps))
        self.assertEqual(0, self.engine.level)
        self.assertEqual(0, self.engine.max_combo)
        self.assertEqual(0, self.engine.score)
        self.assertEqual(0, self.engine.current_combo)
        self.assertEqual(0, self.engine.combo_timer)
        self.assertEqual(0, self.engine.combo_start_time)
        self.assertEqual(0, self.engine.start_time)
        self.assertTrue(self.engine.player_can_do_more_combo)
        self.assertEqual(pygame.font.Font, type(self.engine.font))
        self.assertEqual(1, len(self.steps_group))

    def test_initialisation(self):
        self.check_parameters()

    def test_spawning_steps(self):
        steps_before = self.engine.list_of_steps.copy()

        self.engine.spawning_steps()

        self.assertEqual(len(steps_before), len(self.engine.list_of_steps))
        self.assertNotEqual(steps_before, self.engine.list_of_steps)
        self.assertEqual(5, len(self.steps_group))

    def test_adjust_steps_when_player_is_highly(self):
        steps_heights_before = ([step.step_height for step in self.steps_group]
                                + [step.step_height for step in self.engine.list_of_steps])
        self.player.rect.top = 50
        self.player.y_speed = -5

        self.engine.adjust_steps()
        steps_heights_after = ([step.step_height for step in self.steps_group]
                               + [step.step_height for step in self.engine.list_of_steps])

        self.assertEqual(len(steps_heights_before), len(steps_heights_after))
        for i in range(len(steps_heights_before)):
            self.assertEqual(steps_heights_before[i] + self.player.y_speed, steps_heights_after[i])

        for step in self.steps_group:
            self.assertEqual(step.rect.top, 800 - step.step_height + self.player.current_height)

    def test_adjust_steps_when_player_is_low(self):
        self.player.rect.top = 500
        self.player.y_speed = -5

        self.engine.adjust_steps()

        for step in self.steps_group:
            self.assertEqual(step.rect.top, 800 - step.step_height + self.player.current_height)

    def test_contact_with_steps_when_player_has_contact_with_step(self):
        step = StepSnowbiom(300, 1)
        step.rect.top = 300
        self.steps_group.add(step)
        self.player.rect.bottom = 305
        self.player.rect.centerx = step.rect.centerx
        self.player.y_speed = 1

        self.engine.contact_with_steps()

        self.assertTrue(self.player.can_jump)
        self.assertFalse(self.player.super_jump)
        self.assertEqual(self.player.y_speed, 0)
        self.assertEqual(step.rect.top, self.player.rect.bottom)

    def test_contact_with_steps_when_player_has_not_contact_with_step(self):
        step = StepSnowbiom(300, 1)
        step.rect.top = 300
        self.steps_group.add(step)
        self.player.rect.bottom = 330
        self.player.y_speed = 1

        self.engine.contact_with_steps()

        self.assertFalse(self.player.can_jump)
        self.assertFalse(self.player.super_jump)
        self.assertEqual(self.player.y_speed, 1)
        self.assertEqual(330, self.player.rect.bottom)

    def test_time_destroying_steps_nothing_happen_when_player_on_step_0(self):

        self.engine.time_destroying_steps()

        for step in self.steps_group:
            self.assertFalse(step.destruction)

    @patch('pygame.time.get_ticks', return_value=50000)
    def test_time_destroying_steps_when_player_is_high(self, _):
        self.steps_group.add(StepSnowbiom(300, 1))
        self.steps_group.add(StepSnowbiom(500, 1))
        self.steps_group.add(StepSnowbiom(700, 1))
        self.player.max_height = 300

        self.engine.time_destroying_steps()

        for step in self.engine.my_steps:
            self.assertTrue(step.destruction)

    def test_update_result_saved_combos_when_player_can_not_do_more(self):
        self.engine.combo_start_time = -10000
        self.engine.level = 5
        self.engine.score = 50
        self.engine.current_combo = 5
        step = StepSnowbiom(500, 7)
        self.steps_group.add(step)
        self.player.rect.bottom = 500
        self.player.rect.centerx = step.rect.centerx

        self.engine.update_result()

        self.assertFalse(self.engine.player_can_do_more_combo)
        self.assertEqual(70 + 5 ** 2 * 5, self.engine.score)
        self.assertEqual(5, self.engine.max_combo)
        self.assertEqual(0, self.engine.current_combo)
        self.assertEqual(0, self.engine.combo_start_time)
        self.assertEqual(7, self.engine.level)

    def test_update_result_saved_combos_when_player_can_do_more(self):
        self.engine.combo_start_time = 0
        self.engine.level = 5
        self.engine.score = 50
        step = StepSnowbiom(500, 7)
        self.steps_group.add(step)
        self.player.rect.bottom = 500
        self.player.rect.centerx = step.rect.centerx

        self.engine.update_result()

        self.assertTrue(self.engine.player_can_do_more_combo)
        self.assertEqual(70, self.engine.score)
        self.assertEqual(0, self.engine.max_combo)
        self.assertEqual(2, self.engine.current_combo)
        self.assertNotEqual(0, self.engine.combo_start_time)
        self.assertEqual(7, self.engine.level)

    @patch('engine.Engine._display_text')
    def test_display_result(self, mock_display_text):
        self.engine.display_result()

        mock_display_text.assert_called_once_with(str(self.engine.score), (100, 0))

    @patch('engine.Engine._display_text')
    def test_display_combo_timer_when_combo_timer_equals_0(self, mock_display_text):
        self.engine.display_combo_timer()
        mock_display_text.assert_not_called()

    @patch('engine.Engine._display_text')
    def test_display_combo_timer_when_combo_timer_greater_than_0(self, mock_display_text):
        self.engine.combo_timer = 1000
        self.engine.level = 5

        self.engine.display_combo_timer()

        mock_display_text.assert_called_once_with(str(self.engine.combo_timer), (820, 0))

    @patch('engine.Engine._display_text')
    def test_display_combo_when_combo_equals_0(self, mock_display_text):
        self.engine.display_combo()
        mock_display_text.assert_not_called()

    @patch('engine.Engine._display_text')
    def test_display_combo_when_combo_greater_than_0(self, mock_display_text):
        self.engine.current_combo = 5

        self.engine.display_combo()

        mock_display_text.assert_called_once_with(str(self.engine.current_combo), (850, 50))

    @patch('player.Player.reset')
    def test_reset(self, mock_player):
        self.engine.list_of_steps = [StepSnowbiom(300, 8),
                                     StepSnowbiom(500, 20),
                                     StepSnowbiom(700, 3),
                                     StepSnowbiom(900, 4),
                                     StepSnowbiom(1100, 5)]

        self.engine.my_steps.add(FloorSnowbiom(100, 12))

        self.engine.level = 10
        self.engine.max_combo = 10
        self.engine.score = 10

        self.engine.current_combo = 10
        self.engine.player_can_do_more_combo = False
        self.engine.font = pygame.font.SysFont("Comic Sans MS", 35)
        self.engine.start_time = 2
        self.engine.combo_timer = 2
        self.engine.combo_start_time = 2

        self.engine.reset()

        mock_player.assert_called_once()
        self.check_parameters()

    @patch('engine.Engine.spawning_steps')
    @patch('engine.Engine.adjust_steps')
    @patch('engine.Engine.contact_with_steps')
    @patch('engine.Engine.time_destroying_steps')
    @patch('engine.Engine.update_result')
    @patch('engine.Engine.display_combo_timer')
    @patch('engine.Engine.display_combo')
    @patch('engine.Engine.display_result')
    def test_update(self, mock_display_result, mock_display_combo, mock_display_combo_timer, mock_update_result,
                    mock_time_destroying_steps, mock_contact_with_steps, mock_adjust_steps, mock_spawning_steps):
        mock_screen = MagicMock(spec=pygame.Surface)
        mock_background = MagicMock(spec=pygame.Surface)
        mock_player = MagicMock(spec=pygame.sprite.GroupSingle)
        mock_steps = MagicMock(spec=pygame.sprite.Group)
        self.engine.main_screen = mock_screen
        self.engine.start_background = mock_background
        self.engine.my_player = mock_player
        self.engine.my_steps = mock_steps

        self.engine.update()

        mock_display_result.assert_called_once()
        mock_display_combo.assert_called_once()
        mock_display_combo_timer.assert_called_once()
        mock_update_result.assert_called_once()
        mock_time_destroying_steps.assert_called_once()
        mock_contact_with_steps.assert_called_once()
        mock_adjust_steps.assert_called_once()
        mock_spawning_steps.assert_called_once()
        mock_screen.blit.assert_any_call(mock_background, (0, 0))
        mock_player.draw.assert_called_once_with(mock_screen)
        mock_player.update.assert_called_once()
        mock_steps.draw.assert_called_once_with(mock_screen)
        mock_steps.update.assert_called_once()
