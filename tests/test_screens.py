import unittest
from unittest.mock import patch, MagicMock, Mock
import pygame
import os

import screens
from screens import Intro, RotatePlayer, Floor, AllFloors, Outro


class TestIntro(unittest.TestCase):

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
        self.intro = Intro(self.screen)

    def tearDown(self):
        pygame.quit()

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_init(self, mock_scale, mock_load):
        self.intro = Intro(self.screen)
        self.assertTrue(mock_load.called)
        self.assertTrue(mock_scale.called)

    @patch('pygame.mouse.get_pressed')
    @patch('pygame.mouse.get_pos')
    def test_check_buttons_play(self, mock_get_pos, mock_get_pressed):
        mock_get_pressed.return_value = (1, 0, 0)
        mock_get_pos.return_value = self.intro.play_image_rect.center

        self.intro.check_buttons()
        self.assertTrue(self.intro.play_button)

    @patch('pygame.mouse.get_pressed')
    @patch('pygame.mouse.get_pos')
    def test_check_buttons_help(self, mock_get_pos, mock_get_pressed):
        mock_get_pressed.return_value = (1, 0, 0)
        mock_get_pos.return_value = self.intro.help_image_rect.center

        with patch('builtins.print') as mock_print:
            self.intro.check_buttons()
            mock_print.assert_called_once_with("I can't help you")
            # self.assertTrue(self.intro.play_button)

    @patch('pygame.mouse.get_pressed')
    @patch('pygame.mouse.get_pos')
    @patch('pygame.event.post')
    def test_check_buttons_quit(self, mock_event_post, mock_get_pos, mock_get_pressed):
        mock_get_pressed.return_value = (1, 0, 0)
        mock_get_pos.return_value = self.intro.quit_image_rect.center

        self.intro.check_buttons()
        self.assertTrue(mock_event_post.called)
        event = mock_event_post.call_args[0][0]
        self.assertEqual(event.type, pygame.QUIT)

    @patch('screens.Intro.draw')
    @patch('screens.Intro.check_buttons')
    def test_update(self, mock_check_buttons, mock_draw):
        self.intro.update()
        mock_draw.assert_called_once()
        mock_check_buttons.assert_called_once()


class TestRotatePlayer(unittest.TestCase):

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
        self.player = RotatePlayer()

    def tearDown(self):
        pygame.quit()

    @patch('pygame.image.load')
    @patch('pygame.transform.scale_by')
    def test_init(self, mock_scale, mock_load):
        mock_image = MagicMock()
        mock_image.get_rect.return_value.center = (775, 500)
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        self.player = RotatePlayer()

        self.assertTrue(mock_load.called)
        self.assertTrue(mock_scale.called)
        self.assertIsNotNone(self.player.image)
        self.assertEqual(self.player.rect.center, (775, 500))
        self.assertEqual(self.player.counter, 0)
        self.assertEqual(self.player.angle, 0)

    @patch('pygame.transform.rotate')
    def test_rotate_player(self, mock_rotate):
        angle_before_rotate = self.player.angle

        for _ in range(10):
            self.player.rotate()

        self.assertEqual(self.player.counter, 10)
        self.assertEqual(self.player.angle, (angle_before_rotate + 60) % 360)
        mock_rotate.assert_called_once_with(self.player.original_image, self.player.angle)

    @patch('screens.RotatePlayer.rotate')
    def test_update(self, mock_rotate):
        self.player.update()
        mock_rotate.assert_called_once()


class TestFloor(unittest.TestCase):

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
        self.floor = Floor((0, 0))

    def tearDown(self):
        pygame.quit()

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_init(self, mock_scale, mock_load):
        mock_image = Mock(spec=pygame.Surface)
        mock_image.convert_alpha.return_value = mock_image
        mock_image.get_rect.return_value = pygame.Rect(0, 0, 100, 30)
        mock_load.return_value = mock_image

        mock_scale.return_value = mock_image

        self.floor = Floor((0, 0))

        mock_load.assert_called_once_with('resources/floors/step_snowbiom_0.png')
        mock_scale.assert_called_once_with(mock_image, (100, 30))
        self.assertIsNotNone(self.floor.image)
        self.assertEqual(self.floor.rect.size, (100, 30))

    def test_move_up(self):
        initial_centery = self.floor.rect.centery
        self.floor.move_up()
        self.assertEqual(self.floor.rect.centery, initial_centery - 1)

    @patch('screens.Floor.move_up')
    def test_update(self, mock_move_up):
        self.floor.update()
        mock_move_up.assert_called_once()


class TestAllFloors(unittest.TestCase):

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
        self.all_floors = AllFloors()

    def tearDown(self):
        pygame.quit()

    def _check_conditions(self):
        self.assertIsInstance(self.all_floors.floors_group, pygame.sprite.Group)
        self.assertEqual(len(self.all_floors.floors_group), 4)
        for floor in self.all_floors.floors_group:
            self.assertIsInstance(floor, Floor)
            self.assertLessEqual(floor.rect.top, 800)
            self.assertGreaterEqual(floor.rect.bottom, 0)

    def test_init(self):
        self._check_conditions()

    def test_check_steps(self):
        self.all_floors.check_steps()
        self._check_conditions()

    @patch('screens.AllFloors.check_steps')
    @patch('pygame.sprite.Group.update')
    def test_update(self, mock_update, mock_check_steps):
        self.all_floors.update()
        mock_update.assert_called_once()
        mock_check_steps.assert_called_once()

    @patch('pygame.sprite.Group.draw')
    def test_draw(self, mock_draw):
        self.all_floors.draw(self.screen)
        mock_draw.assert_called_once()


class TestOutro(unittest.TestCase):

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
        self.outro = Outro(self.screen)

    def tearDown(self):
        pygame.quit()

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    @patch('pygame.transform.scale_by')
    @patch('screens.AllFloors')
    @patch('screens.RotatePlayer')
    def test_initialization(self, mock_rotate_player, mock_all_floors, mock_scale_by, mock_scale, mock_load):
        mock_image = Mock(spec=pygame.Surface)
        mock_image.convert_alpha.return_value = mock_image
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image
        mock_scale_by.return_value = mock_image

        mock_all_floors.return_value = Mock(spec=AllFloors)
        mock_rotate_player.return_value = Mock(spec=RotatePlayer)

        outro = Outro(self.screen)

        self.assertEqual(outro.level, 0)
        self.assertEqual(outro.max_combo, 0)
        self.assertEqual(outro.score, 0)
        self.assertEqual(outro.status, "outro")

        mock_load.assert_any_call('resources/backgrounds/background.png')
        mock_load.assert_any_call('resources/backgrounds/restart.png')
        mock_load.assert_any_call('resources/backgrounds/home.png')

        mock_scale.assert_any_call(outro.image, (1000, 800))
        mock_scale_by.assert_any_call(mock_image, 2)

        self.assertIsInstance(outro.rotate_player_group, pygame.sprite.GroupSingle)
        self.assertIsInstance(outro.rotate_player_group.sprite, RotatePlayer)
        self.assertIsInstance(outro.floors_group, AllFloors)

    @patch('pygame.mouse.get_pressed')
    @patch('pygame.mouse.get_pos')
    def test_check_buttons(self, mock_get_pos, mock_get_pressed):
        mock_get_pressed.return_value = (1, 0, 0)

        mock_get_pos.return_value = self.outro.home_image_rect.center
        self.outro.check_buttons()
        self.assertEqual(self.outro.status, "intro")

        mock_get_pos.return_value = self.outro.restart_image_rect.center
        self.outro.check_buttons()
        self.assertEqual(self.outro.status, "game_on")

    # TODO: write tests for methods display_text, draw, update
