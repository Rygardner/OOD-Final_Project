"""mock_game.py

Tests for game.py
"""

import unittest
from unittest.mock import patch, Mock
from hypothesis import given, settings
from hypothesis import strategies as st
import pygame
from game import game
from Levels import Level_Objects


def fake_pygame_init(self) -> None:
    """Fake pygame init so tests do not open a real window
    """
    self.screen = Mock(name="screen")
    self.clock = Mock(name="clock")


class TestGameOOP(unittest.TestCase):
    """Tests for game.py
    """

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        game._instance = None
        game._initialized = False
        return super().tearDown()

    def test_singleton(self) -> None:
        """Creating 2 Game objects twice returns the same instance and checks
        mock player class is called once
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):
            
            mock_player_class.return_value = Mock()
            game_one = game()
            game_two = game()

            self.assertIs(game_one, game_two)
            self.assertTrue(game._initialized)
            mock_player_class.assert_called_once()

    def test_level_setup(self) -> None:
        """Level setup should update objects, player start, and goal position
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):
            
            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        mock_player.x = 0
        mock_player.y = 0
        level_objects = ["platform1", "platform2"]
        new_start_pos = [100, 200]
        new_goal_pos = [400, 500]

        mock_game.level_setup(level_objects, new_start_pos, new_goal_pos)

        self.assertEqual(mock_game.objects, level_objects)
        self.assertEqual(mock_game.start_pos, new_start_pos)
        self.assertEqual(mock_player.x, new_start_pos[0])
        self.assertEqual(mock_player.y, new_start_pos[1])
        self.assertEqual(mock_game.goal_pos, new_goal_pos)
        self.assertEqual(mock_game.goal.x, new_goal_pos[0])
        self.assertEqual(mock_game.goal.y, new_goal_pos[1])

    @given(
           start_x=st.integers(min_value=-10000, max_value=10000),
           start_y=st.integers(min_value=-10000, max_value=10000),
           goal_x=st.integers(min_value=-10000, max_value=10000),
           goal_y=st.integers(min_value=-10000, max_value=10000),
          )
    @settings(max_examples=1000, derandomize=True)
    def test_level_setup_various_positions(self, start_x: int, start_y: int, goal_x: int, goal_y: int,) -> None:
        """Tests level setup with a wide range of position inputs 
        """
        game._instance = None
        game._initialized = False

        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):
            
            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        mock_player.x = 0
        mock_player.y = 0
        mock_level_objects = []

        mock_game.level_setup(mock_level_objects, [start_x, start_y], [goal_x, goal_y])

        self.assertEqual(mock_player.x, start_x)
        self.assertEqual(mock_player.y, start_y)
        self.assertEqual(mock_game.goal.x, goal_x)
        self.assertEqual(mock_game.goal.y, goal_y)

    def test_draw_platforms(self) -> None:
        """Draw platforms draws each object plus the goal, so it should be called
        3 times when drawing 2 objects"""
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with patch("pygame.draw.rect") as mock_draw_rect:
            mock_game.objects = [Mock(), Mock()]
            mock_game.goal = Mock()

            mock_game.draw_platforms()

        self.assertEqual(mock_draw_rect.call_count, 3)

    def test_post_game_menu_win(self) -> None:
        """When winning triggers post game menu and the first button is clicked, it 
        should return 0"""
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch("pygame.Rect") as mock_rect,
              patch("game.button") as mock_button):

            mock_rect.side_effect = [Mock(), Mock(), Mock()]

            button_next = Mock()
            button_select = Mock()
            button_main = Mock()
            button_next.button_clicked.return_value = True
            button_select.button_clicked.return_value = False
            button_main.button_clicked.return_value = False

            mock_button.side_effect = [button_next, button_select, button_main]

            with (patch("pygame.event.get", return_value=[]),
                  patch("pygame.display.flip"),
                  patch.object(mock_game.clock, "tick")):

                result = mock_game.post_game_menu(True)

        self.assertEqual(result, 0)

    def test_post_game_menu_lose_retry_level(self) -> None:
        """When losing triggers post game menu and the first button is clicked, it
        should return 3
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch("pygame.Rect") as mock_rect,
              patch("game.button") as mock_button):

            mock_rect.side_effect = [Mock(), Mock(), Mock()]

            button_retry = Mock()
            button_select = Mock()
            button_main = Mock()
            button_retry.button_clicked.return_value = True
            button_select.button_clicked.return_value = False
            button_main.button_clicked.return_value = False

            mock_button.side_effect = [button_retry, button_select, button_main]

            with (patch("pygame.event.get", return_value=[]),
                  patch("pygame.display.flip"),
                  patch.object(mock_game.clock, "tick")):

                result = mock_game.post_game_menu(False)

        self.assertEqual(result, 3)

    def test_level_select_quit(self) -> None:
        """level_select should call quit when a QUIT event is received
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch.object(Level_Objects, "level_select_buttons", []),
              patch("pygame.event.get", return_value=[Mock(type=pygame.QUIT)]),
              patch.object(mock_game, "quit", side_effect=SystemExit) as mock_quit):

            with self.assertRaises(SystemExit):
                mock_game.level_select()

        mock_quit.assert_called_once()

    def test_post_game_menu_quit(self) -> None:
        """post_game_menu should call quit when a QUIT event is received
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch("pygame.Rect", return_value=Mock()),
              patch("game.button", return_value=Mock()),
              patch("pygame.event.get", return_value=[Mock(type=pygame.QUIT)]),
              patch.object(mock_game, "quit", side_effect=SystemExit) as mock_quit):
            
            with self.assertRaises(SystemExit):
                mock_game.post_game_menu(False)

        mock_quit.assert_called_once()

   