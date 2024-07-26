import unittest
from unittest.mock import patch, MagicMock, Mock
import pygame
import os
import player


class TestPlayer(unittest.TestCase):

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

    @patch('pygame.image.load')
    def test_initialization(self, mock_load):
        mock_image = MagicMock(spec=pygame.Surface)
        mock_image.convert_alpha.return_value = mock_image
        mock_image.get_rect.return_value = MagicMock(spec=pygame.Rect)
        mock_load.return_value = mock_image

        instance = player.Player()

        mock_load.assert_called_once_with("resources/Player/player_stand.png")
        mock_image.get_rect.assert_called_once_with(midbottom=(500, 700))
        self.assertEqual(instance.x_speed, 0)
        self.assertEqual(instance.y_speed, 0)
        self.assertEqual(instance.current_height, 0)
        self.assertEqual(instance.max_height, 0)
        self.assertEqual(instance.counter, 0)
        self.assertEqual(instance.actual_angle, 0)
        self.assertTrue(instance.can_jump)
        self.assertFalse(instance.super_jump)



