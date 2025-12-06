"""mock_game.py

Tests for game.py
"""

import unittest
from unittest.mock import patch, Mock
from hypothesis import given, settings
from hypothesis import strategies as st
import pygame
from game import game
from game import main as game_main
import Level_Objects


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

    @given(start_x=st.integers(min_value=-10000, max_value=10000),
           start_y=st.integers(min_value=-10000, max_value=10000),
           goal_x=st.integers(min_value=-10000, max_value=10000),
           goal_y=st.integers(min_value=-10000, max_value=10000))
    @settings(max_examples=1000, derandomize=True)
    def test_level_setup_various_positions(
            self, start_x: int, start_y: int, goal_x: int, goal_y: int,) -> None:
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
        3 times when drawing 2 objects
        """
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
        should return 0
        """
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

    def test_level_changer_level_setup(self) -> None:
        """Level changer should set up levels 1-6 and call level_setup
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            game_instance = game()

        for level in range(1, 7):
            level_objects = f"objects_for_level_{level}"
            new_start_pos = [level, level + 10]
            new_goal_pos = [level + 20, level + 30]

            with (patch.object(Level_Objects, f"level_{level}_objects", level_objects),
                  patch.object(Level_Objects, f"level_{level}_start_pos", new_start_pos),
                  patch.object(Level_Objects, f"level_{level}_goal_pos", new_goal_pos),
                  patch.object(game, "level_setup") as mock_level_setup):

                result = game_instance.level_changer(level)

            self.assertTrue(result)
            self.assertEqual(game_instance.level, level)
            mock_level_setup.assert_called_once_with(level_objects, new_start_pos, new_goal_pos)

    def test_level_changer_invalid_level(self) -> None:
        """Invalid level should leave current level unchanged and return False
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        mock_game.level = 99
        result = mock_game.level_changer(0)

        self.assertEqual(mock_game.level, 99)
        self.assertFalse(result)

    def test_level_select(self) -> None:
        """level_select should call level_changer and return true
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        level_button = Mock()
        level_button.button_clicked.return_value = True

        with (patch.object(Level_Objects, "level_select_buttons", [level_button]),
              patch("pygame.event.get", side_effect=[[Mock(type=pygame.MOUSEBUTTONUP)], [],]),
              patch("pygame.display.flip"), patch.object(mock_game.clock, "tick"),
              patch.object(mock_game, "level_changer", return_value=True) as mock_level_changer):

            result = mock_game.level_select()

        self.assertTrue(result)
        mock_level_changer.assert_called_once_with(1)
        level_button.draw_button.assert_called_once_with(mock_game.screen)
        level_button.button_clicked.assert_called_once()

    def test_level_select_exit_button(self) -> None:
        """Exit button should return false
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        level_buttons: list[Mock] = []
        for index in range(7):
            button = Mock()
            button.draw_button = Mock()
            button.button_clicked.return_value = (index == 6)
            level_buttons.append(button)

        with (patch.object(Level_Objects, "level_select_buttons", level_buttons),
              patch("pygame.event.get", side_effect=[[Mock(type=pygame.MOUSEBUTTONUP)], [],]),
              patch("pygame.display.flip"), patch.object(mock_game.clock, "tick"),
              patch.object(mock_game, "level_changer") as mock_level_changer):

            result = mock_game.level_select()

        self.assertFalse(result)
        mock_level_changer.assert_not_called()

    def test_main_menu_level_select_button(self) -> None:
        """main_menu should return 1 when level select button is clicked
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch("pygame.Rect") as mock_rect,
              patch("game.button") as mock_button):

            mock_rect.side_effect = [Mock(), Mock()]

            level_select_button = Mock()
            exit_button = Mock()
            level_select_button.button_clicked.return_value = True
            exit_button.button_clicked.return_value = False
            mock_button.side_effect = [level_select_button, exit_button]

            with (patch("pygame.event.get", return_value=[]),
                  patch("pygame.display.flip"),
                  patch.object(mock_game.clock, "tick")):

                result = mock_game.main_menu()

        self.assertEqual(result, 1)

    def test_main_menu_exit_button(self) -> None:
        """main_menu should return 0 when the exit button is clicked
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch("pygame.Rect") as mock_rect,
              patch("game.button") as mock_button):

            mock_rect.side_effect = [Mock(), Mock()]

            level_select_button = Mock()
            exit_button = Mock()
            level_select_button.button_clicked.return_value = False
            exit_button.button_clicked.return_value = True
            mock_button.side_effect = [level_select_button, exit_button]

            with (patch("pygame.event.get", return_value=[]),
                  patch("pygame.display.flip"),
                  patch.object(mock_game.clock, "tick")):

                result = mock_game.main_menu()

        self.assertEqual(result, 0)

    def test_main_menu_flip_tick_and_quit_event(self) -> None:
        """main_menu should flip, tick, and handle QUIT event
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch("pygame.Rect") as mock_rect,
              patch("game.button") as mock_button):

            mock_rect.side_effect = [Mock(), Mock()]

            level_select_button = Mock()
            exit_button = Mock()
            level_select_button.button_clicked.side_effect = [False, True]
            exit_button.button_clicked.return_value = False
            mock_button.side_effect = [level_select_button, exit_button]

            with (patch("pygame.event.get", side_effect=[[], [Mock(type=pygame.QUIT)]]),
                  patch("pygame.display.flip") as mock_flip,
                  patch.object(mock_game.clock, "tick") as mock_tick,
                  patch.object(mock_game, "quit", side_effect=SystemExit) as mock_quit):

                with self.assertRaises(SystemExit):
                    mock_game.main_menu()

        mock_flip.assert_called_once()
        mock_tick.assert_called_once()
        mock_quit.assert_called_once()

    def test_quit_calls_pygame_quit_and_sys_exit(self) -> None:
        """Quit should call pygame.quit and sys.exit
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch("pygame.quit") as mock_pygame_quit,
              patch("sys.exit") as mock_sys_exit):

            mock_game.quit()

        mock_pygame_quit.assert_called_once()
        mock_sys_exit.assert_called_once()

    def test_manager_quit(self) -> None:
        """manager should quit when main_menu returns 0
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch.object(mock_game, "main_menu", return_value=0) as mock_main,
              patch.object(mock_game, "quit", side_effect=SystemExit) as mock_quit):

            with self.assertRaises(SystemExit):
                mock_game.manager()

        mock_main.assert_called_once()
        mock_quit.assert_called_once()

    def test_manager_next_level_on_win(self) -> None:
        """Manager should go level select then next level when game is won
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch.object(mock_game, "main_menu", side_effect=[1]) as mock_main,
              patch.object(mock_game, "level_select", return_value=True) as mock_level_select,
              patch.object(mock_game, "level_changer", return_value=True) as mock_level_changer,
              patch.object(mock_game, "Game_play", side_effect=[0, SystemExit]) as mock_game_play):

            with self.assertRaises(SystemExit):
                mock_game.manager()

        mock_main.assert_called_once()
        mock_level_select.assert_called_once()
        self.assertGreaterEqual(mock_level_changer.call_count, 1)
        self.assertGreaterEqual(mock_game_play.call_count, 2)

    def test_manager_main_menu(self) -> None:
        """Manager should go to main_menu and then quit
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch.object(mock_game, "main_menu", side_effect=[4, 0]) as mock_main,
              patch.object(mock_game, "quit", side_effect=SystemExit) as mock_quit):

            with self.assertRaises(SystemExit):
                mock_game.manager()

        self.assertEqual(mock_main.call_count, 2)
        mock_quit.assert_called_once()

    def test_manager_retry_level(self) -> None:
        """Manager should retry level
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()
            mock_game.level = 2

        with (patch.object(mock_game, "main_menu", side_effect=[1]) as mock_main,
              patch.object(mock_game, "level_select", return_value=True) as mock_level_select,
              patch.object(mock_game, "level_changer", return_value=True) as mock_level_changer,
              patch.object(mock_game, "Game_play", side_effect=[3, SystemExit]) as mock_game_play):

            with self.assertRaises(SystemExit):
                mock_game.manager()

        mock_main.assert_called_once()
        mock_level_select.assert_called_once()
        self.assertEqual(mock_level_changer.call_count, 1)
        self.assertGreaterEqual(mock_game_play.call_count, 2)

    def test_manager_returns_to_main_menu_from_level_select(self) -> None:
        """Manager should return to main menu from level select
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        with (patch.object(mock_game, "main_menu", side_effect=[1, 0]) as mock_main,
              patch.object(mock_game, "level_select", return_value=False) as mock_level_select,
              patch.object(mock_game, "Game_play") as mock_game_play,
              patch.object(mock_game, "quit", side_effect=SystemExit) as mock_quit):

            with self.assertRaises(SystemExit):
                mock_game.manager()

        self.assertEqual(mock_main.call_count, 2)
        mock_level_select.assert_called_once()
        mock_game_play.assert_not_called()
        mock_quit.assert_called_once()

    def test_main_exception(self) -> None:
        """Main should catch exception and print it
        """
        with (patch("game.game") as mock_game_class,
              patch("builtins.print") as mock_print):

            instance = Mock()
            instance.manager.side_effect = RuntimeError("boom")
            mock_game_class.return_value = instance

            game_main()

        mock_game_class.assert_called_once()
        instance.manager.assert_called_once()
        mock_print.assert_called_once()
        args, _ = mock_print.call_args
        self.assertIn("CRASH:", args[0])

    def test_pygame_init(self) -> None:
        """Test pygame initializes a window
        """
        with (patch("pygame.init") as mock_init,
              patch("pygame.display.init") as mock_display_init,
              patch("pygame.font.init") as mock_font_init,
              patch("pygame.display.set_mode") as mock_set_mode,
              patch("pygame.display.set_caption") as mock_set_caption,
              patch("pygame.time.Clock") as mock_clock_cls,
              patch("pygame.display.flip") as mock_flip,
              patch("pygame.time.delay") as mock_delay):

            fake_screen = Mock()
            fake_clock = Mock()
            mock_set_mode.return_value = fake_screen
            mock_clock_cls.return_value = fake_clock

            game_instance = game.__new__(game)

            game.pygame_init(game_instance)

            mock_init.assert_called_once()
            mock_display_init.assert_called_once()
            mock_font_init.assert_called_once()
            mock_set_mode.assert_called_once()
            mock_set_caption.assert_called_once()
            self.assertIs(game_instance.screen, fake_screen)
            self.assertIs(game_instance.clock, fake_clock)
            mock_flip.assert_called_once()
            mock_delay.assert_called_once()

    def test_game_play(self) -> None:
        """game_play should update, fill, draw, flip, and tick.
        game_play goes through 2 iterations in it's current state
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock()
            mock_player_class.return_value = mock_player
            mock_game = game()

        mock_player.rect = Mock()
        mock_player.rect.colliderect.return_value = False
        mock_player.update = Mock()
        mock_player.draw = Mock()

        mock_game.goal = Mock()
        mock_game.floor = Mock()
        mock_game.objects = []

        with (patch("pygame.event.get", side_effect=[[], [Mock(type=pygame.QUIT)]]),
              patch("pygame.key.get_pressed", return_value=Mock()) as mock_keypress,
              patch.object(mock_game.screen, "fill") as mock_fill,
              patch.object(mock_game, "draw_platforms") as mock_draw_platforms,
              patch("pygame.display.flip") as mock_flip,
              patch.object(mock_game.clock, "tick") as mock_tick,
              patch.object(mock_game, "post_game_menu", return_value=2)):

            result = mock_game.Game_play()

        self.assertEqual(result, 2)

        self.assertEqual(mock_keypress.call_count, 2)
        self.assertEqual(mock_player.update.call_count, 2)
        self.assertEqual(mock_fill.call_count, 2)
        self.assertEqual(mock_draw_platforms.call_count, 2)
        self.assertEqual(mock_player.draw.call_count, 2)
        self.assertEqual(mock_flip.call_count, 2)
        self.assertEqual(mock_tick.call_count, 2)

    def test_game_play_goal(self) -> None:
        """When player collides with goal win should be true
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        mock_player.rect = Mock()
        mock_player.rect.colliderect.side_effect = [True, False]
        mock_player.update = Mock()
        mock_player.draw = Mock()

        mock_game.goal = Mock()
        mock_game.floor = Mock()
        mock_game.objects = []

        with (patch("pygame.event.get", return_value=[]),
              patch("pygame.key.get_pressed", return_value=Mock()),
              patch.object(mock_game, "draw_platforms"),
              patch("pygame.display.flip"),
              patch.object(mock_game.clock, "tick"),
              patch.object(mock_game, "post_game_menu", return_value=0) as mock_post):

            result = mock_game.Game_play()

        self.assertEqual(result, 0)
        mock_post.assert_called_once_with(True)

    def test_game_player_fall_off(self) -> None:
        """When player falls off win should be false
        """
        with (patch.object(game, "pygame_init", fake_pygame_init),
              patch("game.Player") as mock_player_class):

            mock_player = Mock(name="player")
            mock_player_class.return_value = mock_player
            mock_game = game()

        mock_player.rect = Mock()
        mock_player.rect.colliderect.side_effect = [False, True]
        mock_player.update = Mock()
        mock_player.draw = Mock()
        mock_game.player = mock_player

        mock_game.goal = Mock()
        mock_game.floor = Mock()
        mock_game.objects = []

        with (patch("pygame.event.get", return_value=[]),
              patch("pygame.key.get_pressed", return_value=Mock()),
              patch.object(mock_game, "draw_platforms"),
              patch("pygame.display.flip"),
              patch.object(mock_game.clock, "tick"),
              patch.object(mock_game, "post_game_menu", return_value=3) as mock_post):

            result = mock_game.Game_play()

        self.assertEqual(result, 3)
        mock_post.assert_called_once_with(False)
