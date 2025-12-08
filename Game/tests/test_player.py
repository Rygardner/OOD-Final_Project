import unittest
from unittest.mock import Mock, patch
from player import Player
import pygame


# =========================
# Player Initialization Tests
# =========================
class TestPlayerInitialization(unittest.TestCase):
    @patch("player.pygame.Rect")
    def test_default_initialization(self, mock_rect):
        mock_rect.return_value = Mock()
        player = Player()
        self.assertIsNotNone(player.rect)
        print(player.color)
        self.assertEqual(player.color, (0, 128, 255))
        self.assertEqual(player.move_speed, 5)
        self.assertEqual(player.jump_speed, 15.0)
        self.assertEqual(player.fall_speed, .7)
        self.assertFalse(player.on_ground)
        self.assertFalse(player.touching_left_wall)
        self.assertFalse(player.touching_right_wall)


# =========================
# Player Properties Tests
# =========================
class TestPlayerProperties(unittest.TestCase):
    @patch("player.pygame.Rect")
    def setUp(self, mock_rect):
        mock_rect.return_value = Mock()
        self.player = Player()

    def test_color_property(self):
        self.player.color = (0, 255, 0)
        self.assertEqual(self.player.color, (0, 255, 0))

    def test_move_speed(self):
        self.player.move_speed = 8
        self.assertEqual(self.player.move_speed, 8)

    def test_jump_speed(self):
        self.player.jump_speed = 12.0
        self.assertEqual(self.player.jump_speed, 12.0)

    def test_fall_speed(self):
        self.player.fall_speed = 6.0
        self.assertEqual(self.player.fall_speed, 6.0)

    def test_wall_jump_speed(self):
        self.player.wall_jump_speed = 9.0
        self.assertEqual(self.player.wall_jump_speed, 9.0)

    def test_on_ground_flag(self):
        self.player.on_ground = True
        self.assertTrue(self.player.on_ground)

    def test_movement_strategy_property(self):
        strategy = Mock()
        self.player.movement_strategy = strategy
        self.assertEqual(self.player.movement_strategy, strategy)

    def test_wall_flags(self):
        self.player.touching_left_wall = True
        self.player.touching_right_wall = True
        self.assertTrue(self.player.touching_left_wall)
        self.assertTrue(self.player.touching_right_wall)


# =========================
# Player Movement Tests
# =========================
class TestPlayerMovement(unittest.TestCase):
    @patch("player.pygame.Rect")
    def setUp(self, mock_rect):
        self.rect = Mock()
        mock_rect.return_value = self.rect
        self.player = Player()

    def test_horizontal_collision_left_right(self):
        self.player.touching_left_wall = True
        self.player.touching_right_wall = True
        self.assertTrue(self.player.touching_left_wall)
        self.assertTrue(self.player.touching_right_wall)


# =========================
# Player Jump & Gravity Tests
# =========================
class TestPlayerJumpGravity(unittest.TestCase):
    @patch("player.pygame.Rect")
    def setUp(self, mock_rect):
        self.rect = Mock()
        self.rect.x = 100     # << Fix: numeric x
        self.rect.y = 50      # << Fix: numeric y
        mock_rect.return_value = self.rect

        self.player = Player()
        self.player.on_ground = True

    def test_jump_from_ground(self):
        keys = {
            pygame.K_SPACE: True,
            pygame.K_LEFT: False,
            pygame.K_a: False,
            pygame.K_RIGHT: False,
            pygame.K_d: False
        }
        self.player.jump(keys)
        self.player.update(keys, colliders=[])
        self.assertFalse(self.player.on_ground)

    def test_apply_gravity(self):
        self.player.y = 50
        self.player.jump_velocity = 0.0
        self.player.apply_gravity()
        self.assertEqual(self.player.jump_velocity , self.player.fall_speed)

    def test_wall_jump(self):
        self.player.touching_left_wall = True
        self.player.touching_right_wall = False
        self.assertTrue(self.player.can_wall_jump)


class TestPlayerColorAndRectValidation(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_color_valid_string(self):
        # According to current implementation, final color ends up as the string
        self.player.color = "red"
        self.assertEqual(self.player.color, "red")

    def test_color_invalid_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.player.color = "purple"

    def test_color_invalid_tuple_raises_type_error(self):
        with self.assertRaises(TypeError):
            # length != 3
            self.player.color = (255, 0)

    def test_rect_setter_requires_x_and_y(self):
        class NoXY:
            pass
        with self.assertRaises(TypeError):
            self.player.rect = NoXY()


class TestPlayerCoordinateAndSizeSetters(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_x_setter_type_error(self):
        with self.assertRaises(TypeError):
            self.player.x = 10.5

    def test_y_setter_type_error(self):
        with self.assertRaises(TypeError):
            self.player.y = "20"

    def test_size_setter_valid(self):
        new_size = (50, 60)
        self.player.size = new_size
        self.assertEqual(self.player.size, new_size)

    def test_size_setter_invalid_type(self):
        with self.assertRaises(TypeError):
            self.player.size = "not a tuple"

    def test_size_setter_invalid_tuple_contents(self):
        with self.assertRaises(TypeError):
            self.player.size = (10, -5)


class TestPlayerSpeedAndFlagValidation(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_move_speed_type_error(self):
        with self.assertRaises(TypeError):
            self.player.move_speed = 5.0

    def test_jump_speed_type_error(self):
        with self.assertRaises(TypeError):
            self.player.jump_speed = 10  # must be float

    def test_fall_speed_type_error(self):
        with self.assertRaises(TypeError):
            self.player.fall_speed = 1  # must be float

    def test_wall_jump_speed_type_error(self):
        with self.assertRaises(TypeError):
            self.player.wall_jump_speed = 7  # must be float

    def test_jump_velocity_type_error(self):
        with self.assertRaises(TypeError):
            self.player.jump_velocity = 3  # must be float

    def test_on_ground_type_error(self):
        with self.assertRaises(TypeError):
            self.player.on_ground = "yes"

    def test_can_wall_jump_type_error(self):
        with self.assertRaises(TypeError):
            self.player.can_wall_jump = 1

    def test_touching_left_wall_type_error(self):
        with self.assertRaises(TypeError):
            self.player.touching_left_wall = "no"

    def test_touching_right_wall_type_error(self):
        with self.assertRaises(TypeError):
            self.player.touching_right_wall = 0

    def test_movement_strategy_type_error(self):
        with self.assertRaises(TypeError):
            self.player.movement_strategy = object()  # no get_horizontal_velocity


class TestHorizontalCollisionsRealRect(unittest.TestCase):
    def setUp(self):
        # Use real pygame.Rect for proper collision behavior
        self.player = Player(x=0, y=0, rec_size=(10, 10))

    def test_horizontal_collision_moving_right(self):
        # Overlapping collider to the right
        collider = pygame.Rect(5, 0, 10, 10)
        self.player.handle_horizontal_collisions([collider], horizontal_velocity=5)
        self.assertTrue(self.player.touching_right_wall)
        self.assertFalse(self.player.touching_left_wall)
        self.assertEqual(self.player.rect.right, collider.left)

    def test_horizontal_collision_moving_left(self):
        # Player to the right of collider
        self.player.x = 10
        collider = pygame.Rect(0, 0, 10, 10)

        # Simulate movement left *by applying the velocity first*
        self.player.rect.x += -5  # now at x = 5, overlapping collider (0–10)

        # Now resolve collision
        self.player.handle_horizontal_collisions([collider], horizontal_velocity=-5)

        # Should now snap left side to collider.right and set touching_left_wall
        self.assertTrue(self.player.touching_left_wall)
        self.assertEqual(self.player.rect.left, collider.right)

    def test_horizontal_collision_no_contact_resets_flags(self):
        self.player.touching_left_wall = True
        self.player.touching_right_wall = True
        collider = pygame.Rect(100, 100, 10, 10)  # far away
        self.player.handle_horizontal_collisions([collider], horizontal_velocity=5)
        self.assertFalse(self.player.touching_left_wall)
        self.assertFalse(self.player.touching_right_wall)


class TestJumpLogic(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_jump_from_ground_sets_velocity(self):
        self.player.on_ground = True
        self.player.jump_speed = 10.0
        keys = {pygame.K_SPACE: True}
        self.player.jump(keys)
        self.assertEqual(self.player.jump_velocity, -self.player.jump_speed)
        self.assertFalse(self.player.on_ground)
        self.assertTrue(self.player.can_wall_jump)

    def test_wall_jump_when_allowed(self):
        self.player.on_ground = False
        self.player.can_wall_jump = True
        self.player.touching_left_wall = True
        self.player.wall_jump_speed = 8.0
        keys = {pygame.K_SPACE: True}
        self.player.jump(keys)
        self.assertEqual(self.player.jump_velocity, -self.player.wall_jump_speed)
        self.assertFalse(self.player.can_wall_jump)

    def test_wall_jump_not_allowed_does_nothing(self):
        self.player.on_ground = False
        self.player.can_wall_jump = False
        self.player.touching_left_wall = True
        old_velocity = self.player.jump_velocity
        keys = {pygame.K_SPACE: True}
        self.player.jump(keys)
        self.assertEqual(self.player.jump_velocity, old_velocity)


class TestVerticalCollisionsRealRect(unittest.TestCase):
    def setUp(self):
        self.player = Player(x=0, y=0, rec_size=(10, 10))

    def test_landing_on_platform(self):
        floor = pygame.Rect(0, 10, 50, 10)
        self.player.y = 5  # overlapping: player bottom at 15
        self.player.jump_velocity = 5.0  # falling
        self.player.handle_vertical_collision([floor])
        self.assertEqual(self.player.rect.bottom, floor.top)
        self.assertEqual(self.player.jump_velocity, 0.0)
        self.assertTrue(self.player.on_ground)
        self.assertTrue(self.player.can_wall_jump)

    def test_hitting_ceiling(self):
        ceiling = pygame.Rect(0, 0, 50, 10)
        self.player.y = 5  # overlapping: player top=5, bottom=15
        self.player.jump_velocity = -5.0  # moving up
        self.player.handle_vertical_collision([ceiling])
        self.assertEqual(self.player.rect.top, ceiling.bottom)
        self.assertEqual(self.player.jump_velocity, 0.0)
        # on_ground should remain False for ceiling hit
        self.assertFalse(self.player.on_ground)

    def test_no_vertical_collision_leaves_on_ground_false(self):
        self.player.y = 0
        self.player.jump_velocity = 5.0
        far_floor = pygame.Rect(0, 100, 50, 10)
        self.player.handle_vertical_collision([far_floor])
        self.assertFalse(self.player.on_ground)


class TestReposition(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_reposition_valid(self):
        # Set some non-default state first
        self.player.on_ground = True
        self.player.touching_left_wall = True
        self.player.touching_right_wall = True
        self.player.can_wall_jump = False
        self.player.jump_velocity = 5.0

        self.player.reposition(100, 200)
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 200)
        self.assertEqual(self.player.jump_velocity, 0.0)
        self.assertFalse(self.player.on_ground)
        self.assertFalse(self.player.touching_left_wall)
        self.assertFalse(self.player.touching_right_wall)
        self.assertTrue(self.player.can_wall_jump)

    def test_reposition_invalid_coordinates_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.player.reposition(1.5, 0)
        with self.assertRaises(TypeError):
            self.player.reposition(10, "20")


class TestUpdateFlow(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        # Simple strategy that always moves by +3

        class SimpleStrategy:
            def get_horizontal_velocity(self_inner, move_speed, keys):
                return 3
        self.player.movement_strategy = SimpleStrategy()

    def test_update_calls_movement_and_physics(self):
        start_x = self.player.x
        keys = {pygame.K_SPACE: False}
        colliders = []
        self.player.update(keys, colliders)
        # x should have increased by horizontal velocity
        self.assertEqual(self.player.x, start_x + 3)


class TestPlayerRepositionUpdateDraw(unittest.TestCase):
    @patch("player.pygame.Rect")
    @patch("player.pygame.draw.rect")
    def setUp(self, mock_draw, mock_rect):
        self.mock_draw = mock_draw

        # mock rect position
        self.rect = Mock()
        self.rect.x = 100
        self.rect.y = 50
        mock_rect.return_value = self.rect

        self.player = Player()
        self.player.movement_strategy = Mock()
        self.player.movement_strategy.get_horizontal_velocity.return_value = 0

    def test_reposition_assigns_new_rect(self):
        new_rect = pygame.Rect(50, 60, 10, 10)
        self.player.rect = new_rect
        self.assertIs(self.player.rect, new_rect)
        self.assertEqual(self.player.rect.topleft, (50, 60))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
