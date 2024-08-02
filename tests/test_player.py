import unittest
from unittest.mock import patch, MagicMock
import pygame
import os

from parameterized import parameterized

import player
from constants import LEFT_WALL_COORDINATE, RIGHT_WALL_COORDINATE

os.environ["SDL_VIDEODRIVER"] = "dummy"


class TestPlayer(unittest.TestCase):

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
        self.player = player.Player()

    def tearDown(self):
        pygame.quit()

    @patch('pygame.transform.flip')
    @patch('pygame.image.load')
    def test_initialization(self, mock_load, mock_flip):
        mock_image = MagicMock(spec=pygame.Surface)
        mock_image.convert_alpha.return_value = mock_image
        mock_image.get_rect.return_value = MagicMock(spec=pygame.Rect)
        mock_load.return_value = mock_image
        mock_flip.return_value = mock_image

        instance = player.Player()

        mock_load.assert_any_call("resources/Player/player_stand.png")
        mock_load.assert_any_call("resources/Player/player_walk_1.png")
        mock_flip.called_once_with(instance.player_facing_right, True, False)
        mock_image.get_rect.assert_called_once_with(midbottom=(500, 700))

        self.assertEqual(instance.x_speed, 0)
        self.assertEqual(instance.y_speed, 0)
        self.assertEqual(instance.current_height, 0)
        self.assertEqual(instance.max_height, 0)
        self.assertEqual(instance.counter, 0)
        self.assertEqual(instance.actual_angle, 0)
        self.assertTrue(instance.can_jump)
        self.assertFalse(instance.super_jump)
        self.assertTrue(instance.can_move_horizontally, 0)
        self.assertEqual(instance.around_delay_counter, 0)
        self.assertEqual(instance.direction, 'forward')
        self.assertEqual(instance.ignore_buttons_counter['left'], 0)
        self.assertEqual(instance.ignore_buttons_counter['right'], 0)
        self.assertTrue(instance.is_alive)
        self.assertTrue(instance.can_do_more_combo)

    @parameterized.expand([
        ("test_player_input_jump_with_K_UP", {pygame.K_UP: True, pygame.K_SPACE: False, pygame.K_LEFT: False,
                                              pygame.K_RIGHT: False}),
        ("test_player_input_jump_with_K_SPACE", {pygame.K_UP: False, pygame.K_SPACE: True, pygame.K_LEFT: False,
                                                 pygame.K_RIGHT: False}),
    ])
    @patch('pygame.key.get_pressed')
    def test_player_input_jump(self, _, key_states, mock_get_pressed):
        mock_get_pressed.return_value = key_states

        self.player.player_input()

        self.assertEqual(self.player.direction, 'forward')
        self.assertEqual(self.player.y_speed, -7)
        self.assertFalse(self.player.can_jump)
        self.assertFalse(self.player.super_jump)

    @parameterized.expand([
        ("test_player_input_jump_with_negative_speed", {pygame.K_UP: True, pygame.K_SPACE: False, pygame.K_LEFT: False,
                                                        pygame.K_RIGHT: False}, 8),
        ("test_player_input_jump_with_positive_speed", {pygame.K_UP: False, pygame.K_SPACE: True, pygame.K_LEFT: False,
                                                        pygame.K_RIGHT: False}, -8),
    ])
    @patch('pygame.key.get_pressed')
    def test_player_input_super_jump(self, _, key_states, speed, mock_get_pressed):
        mock_get_pressed.return_value = key_states
        self.player.x_speed = speed

        self.player.player_input()

        self.assertEqual(self.player.direction, 'forward')
        self.assertEqual(self.player.y_speed, -12)
        self.assertFalse(self.player.can_jump)
        self.assertTrue(self.player.super_jump)

    @patch('pygame.key.get_pressed')
    def test_player_input_K_LEFT(self, mock_get_pressed):
        mock_get_pressed.return_value = {pygame.K_UP: False, pygame.K_SPACE: False, pygame.K_LEFT: True,
                                         pygame.K_RIGHT: False}

        rect_left = self.player.rect.left

        for _ in range(10):
            self.player.player_input()

        self.assertEqual(self.player.direction, 'left')
        self.assertAlmostEqual(self.player.x_speed, -1.5, places=3)
        self.assertLess(self.player.rect.left, rect_left)

    @patch('pygame.key.get_pressed')
    def test_player_input_K_RIGHT(self, mock_get_pressed):
        mock_get_pressed.return_value = {pygame.K_UP: False, pygame.K_SPACE: False, pygame.K_LEFT: False,
                                         pygame.K_RIGHT: True}

        rect_left = self.player.rect.left

        for _ in range(10):
            self.player.player_input()

        self.assertEqual(self.player.direction, 'right')
        self.assertAlmostEqual(self.player.x_speed, 1.5, places=3)
        self.assertGreater(self.player.rect.left, rect_left)

    @patch('pygame.key.get_pressed')
    def test_player_input_slow_down(self, mock_get_pressed):
        mock_get_pressed.return_value = {pygame.K_UP: False, pygame.K_SPACE: False, pygame.K_LEFT: False,
                                         pygame.K_RIGHT: False}

        self.player.x_speed = 1
        self.player.direction = 'left'

        for _ in range(10):
            self.player.player_input()

        self.assertEqual(self.player.direction, 'forward')
        self.assertEqual(self.player.x_speed, 0)

    @parameterized.expand([
        ('test_player_cannot_move_through_left_wall', {pygame.K_UP: False, pygame.K_SPACE: False, pygame.K_LEFT: True,
                                                       pygame.K_RIGHT: False}),
        ('test_player_cannot_move_through_right_wall', {pygame.K_UP: False, pygame.K_SPACE: False, pygame.K_LEFT: False,
                                                        pygame.K_RIGHT: True})
    ])
    @patch('pygame.key.get_pressed')
    def test_player_cannot_move_through_wall(self, _, keys, mock_get_pressed):
        mock_get_pressed.return_value = keys

        for _ in range(100):
            self.player.player_input()

        self.assertLessEqual(self.player.rect.right, RIGHT_WALL_COORDINATE)
        self.assertGreaterEqual(self.player.rect.left, LEFT_WALL_COORDINATE)

    def test_apply_gravity_no_effect_on_floor(self):
        centery_before_apply_gravity = self.player.rect.centery

        self.player.apply_gravity()

        self.assertTrue(self.player.can_jump)
        self.assertEqual(self.player.rect.centery, centery_before_apply_gravity)
        self.assertEqual(self.player.y_speed, 0)
        self.assertEqual(self.player.actual_angle, 0)
        self.assertEqual(self.player.counter, 0)
        self.assertFalse(self.player.super_jump)

    def test_apply_gravity_moves_player_down(self):
        y_speed_before_apply_gravity = -7
        self.player.y_speed = y_speed_before_apply_gravity
        self.player.can_jump = False

        self.player.apply_gravity()

        self.assertGreater(self.player.y_speed, y_speed_before_apply_gravity)

    def test_gravity_moves_and_rotates_player_with_super_jump(self):
        y_speed_before_apply_gravity = -12
        angle_before_apply_gravity = 0
        self.player.y_speed = y_speed_before_apply_gravity
        self.player.can_jump = False
        self.player.super_jump = True

        for _ in range(5):
            self.player.apply_gravity()

        self.assertGreater(self.player.y_speed, y_speed_before_apply_gravity)
        self.assertEqual(self.player.actual_angle, angle_before_apply_gravity + 60)

    def test_height_status(self):
        y_speed_before_apply_gravity = -7
        current_height_before_apply_gravity_and_height_status = self.player.current_height
        self.player.y_speed = y_speed_before_apply_gravity
        self.player.can_jump = False

        self.player.height_status()
        self.player.apply_gravity()

        self.assertEqual(self.player.current_height,
                         current_height_before_apply_gravity_and_height_status - y_speed_before_apply_gravity)
        self.assertGreaterEqual(self.player.max_height, self.player.current_height)

    def test_player_rest(self):
        instance = player.Player()
        self.player.x_speed = 10
        self.player.direction = 'right'

        self.player.reset()

        self.assertEqual(instance.x_speed, self.player.x_speed)
        self.assertEqual(instance.y_speed, self.player.y_speed)
        self.assertEqual(instance.current_height, self.player.current_height)
        self.assertEqual(instance.max_height, self.player.max_height)
        self.assertEqual(instance.counter, self.player.counter)
        self.assertEqual(instance.actual_angle, self.player.actual_angle)
        self.assertEqual(instance.around_delay_counter, self.player.around_delay_counter)
        self.assertEqual(instance.direction, self.player.direction)
        self.assertEqual(instance.ignore_buttons_counter['left'], self.player.ignore_buttons_counter['left'])
        self.assertEqual(instance.ignore_buttons_counter['right'], self.player.ignore_buttons_counter['right'])
        self.assertEqual(self.player.rect.midbottom, instance.rect.midbottom)
        self.assertEqual(instance.can_jump, self.player.can_jump)
        self.assertEqual(instance.super_jump, self.player.super_jump)
        self.assertEqual(instance.can_move_horizontally, self.player.can_move_horizontally)
        self.assertEqual(instance.is_alive, self.player.is_alive)
        self.assertTrue(instance.can_do_more_combo)

    def test_check_player_alive(self):
        self.player.rect.top = 801

        self.player.check_player_alive()

        self.assertFalse(self.player.is_alive)

    @patch('player.Player.check_player_alive')
    @patch('player.Player.player_input')
    @patch('player.Player.height_status')
    @patch('player.Player.apply_gravity')
    def test_update(self, mock_apply_gravity, mock_height_status, mock_player_input, mock_check_player_alive):

        self.player.update()

        mock_apply_gravity.assert_called_once()
        mock_height_status.assert_called_once()
        mock_player_input.assert_called_once()
        mock_check_player_alive.assert_called_once()
