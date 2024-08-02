import unittest
from unittest.mock import patch, MagicMock, Mock
import pygame
import os

import screens


class TestIntro(unittest.TestCase):

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
        self.intro = screens.Intro(self.screen)

    def tearDown(self):
        pygame.quit()

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_initialization(self, mock_scale, mock_load):
        self.intro = screens.Intro(self.screen)
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
        self.player = screens.RotatePlayer()

    def tearDown(self):
        pygame.quit()

    @patch('pygame.image.load')
    @patch('pygame.transform.scale_by')
    def test_initialization(self, mock_scale, mock_load):
        mock_image = MagicMock()
        mock_image.get_rect.return_value.center = (775, 500)
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        self.player = screens.RotatePlayer()

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
        self.floor = screens.Floor((0, 0))

    def tearDown(self):
        pygame.quit()

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_initialization(self, mock_scale, mock_load):
        mock_image = Mock(spec=pygame.Surface)
        mock_image.convert_alpha.return_value = mock_image
        mock_image.get_rect.return_value = pygame.Rect(0, 0, 100, 30)
        mock_load.return_value = mock_image

        mock_scale.return_value = mock_image

        self.floor = screens.Floor((0, 0))

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
        self.all_floors = screens.AllFloors()

    def tearDown(self):
        pygame.quit()

    def _check_conditions(self):
        self.assertIsInstance(self.all_floors.floors_group, pygame.sprite.Group)
        self.assertEqual(len(self.all_floors.floors_group), 4)
        for floor in self.all_floors.floors_group:
            self.assertIsInstance(floor, screens.Floor)
            self.assertLessEqual(floor.rect.top, 800)
            self.assertGreaterEqual(floor.rect.bottom, 0)

    def test_initialization(self):
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
        self.outro = screens.Outro(self.screen)

    def tearDown(self):
        pygame.quit()

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    @patch('pygame.transform.scale_by')
    def test_initialization(self, mock_scale_by, mock_scale, mock_load):
        mock_image = Mock(spec=pygame.Surface)
        mock_image.convert_alpha.return_value = mock_image
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image
        mock_scale_by.return_value = mock_image

        outro = screens.Outro(self.screen)

        self.assertEqual(outro.level, 0)
        self.assertEqual(outro.max_combo, 0)
        self.assertEqual(outro.score, 0)
        self.assertEqual(outro.status, "outro")

        mock_load.assert_any_call('resources/backgrounds/background.png')
        mock_load.assert_any_call('resources/buttons/restart.png')
        mock_load.assert_any_call('resources/buttons/home.png')

        mock_scale.assert_any_call(outro.image, (1000, 800))
        mock_scale_by.assert_any_call(mock_image, 2)

        self.assertIsInstance(outro.rotate_player_group, pygame.sprite.GroupSingle)
        self.assertIsInstance(outro.rotate_player_group.sprite, screens.RotatePlayer)
        self.assertIsInstance(outro.floors_group, screens.AllFloors)

    @patch('pygame.mouse.get_pressed')
    @patch('pygame.mouse.get_pos')
    def test_check_buttons_home_button(self, mock_get_pos, mock_get_pressed):
        mock_get_pressed.return_value = (1, 0, 0)

        mock_get_pos.return_value = self.outro.home_image_rect.center
        self.outro.check_buttons()
        self.assertEqual(self.outro.status, "intro")

    @patch('pygame.mouse.get_pressed')
    @patch('pygame.mouse.get_pos')
    def test_check_buttons_home_button(self, mock_get_pos, mock_get_pressed):
        mock_get_pressed.return_value = (1, 0, 0)

        mock_get_pos.return_value = self.outro.restart_image_rect.center
        self.outro.check_buttons()
        self.assertEqual(self.outro.status, "game_on")

    def test_display_text(self):
        mock_screen = MagicMock(spec=pygame.Surface)
        mock_font = MagicMock(spec=pygame.font.Font)
        mock_text_surface = MagicMock(spec=pygame.Surface)
        mock_rect = Mock()
        self.outro.main_screen = mock_screen

        mock_font.render.return_value = mock_text_surface
        mock_text_surface.get_rect.return_value = mock_rect

        self.outro.display_text("Hello World!", mock_font, (10, 20))

        mock_font.render.assert_called_once_with("Hello World!", True, "Brown")
        mock_text_surface.get_rect.assert_called_once_with(topleft=(10, 20))
        mock_screen.blit.assert_called_once_with(mock_text_surface, mock_rect)

    @patch('screens.Outro.display_text')
    def test_draw(self, mock_display_text):
        mock_screen = MagicMock(spec=pygame.Surface)
        mock_player_group = MagicMock(spec=pygame.sprite.Group)
        mock_floors_group = MagicMock(spec=pygame.sprite.Group)

        self.outro.rotate_player_group = mock_player_group
        self.outro.floors_group = mock_floors_group
        self.outro.main_screen = mock_screen

        self.outro.draw()

        mock_screen.blit.assert_any_call(self.outro.image, self.outro.rect)
        mock_screen.blit.assert_any_call(self.outro.restart_image, self.outro.restart_image_rect)
        mock_screen.blit.assert_any_call(self.outro.home_image, self.outro.home_image_rect)
        mock_player_group.draw.assert_called_once_with(self.outro.main_screen)
        mock_floors_group.draw.assert_called_once_with(self.outro.main_screen)
        self.assertEqual(mock_display_text.call_count, 5)

    @patch('screens.Outro.check_buttons')
    @patch('screens.Outro.draw')
    def check_update(self, mock_draw, mock_check_buttons):
        mock_player_group = MagicMock(spec=pygame.sprite.Group)
        mock_floors_group = MagicMock(spec=pygame.sprite.Group)
        self.outro.rotate_player_group = mock_player_group
        self.outro.floors_group = mock_floors_group

        self.outro.update()

        mock_player_group.update.assert_called_once()
        mock_floors_group.update.assert_called_once()
        mock_check_buttons.assert_called_once()
        mock_draw.assert_called_once()
