# test_movement_strategy.py

import pytest
from unittest.mock import MagicMock
import pygame
from movement_strategy import MovementStrategy, NormalMovement, NoMovement


def test_cannot_instantiate_abstract_class():
    # MovementStrategy is abstract, so instantiating should raise TypeError
    with pytest.raises(TypeError):
        MovementStrategy()


def test_normal_movement_left_arrow():
    keys = MagicMock()
    keys.__getitem__.side_effect = lambda k: k == pygame.K_LEFT  # Only left is pressed
    strategy = NormalMovement()
    assert strategy.get_horizontal_velocity(5, keys) == -5


def test_normal_movement_left_a_key():
    keys = MagicMock()
    keys.__getitem__.side_effect = lambda k: k == pygame.K_a  # Only 'A' is pressed
    strategy = NormalMovement()
    assert strategy.get_horizontal_velocity(7, keys) == -7


def test_normal_movement_right_arrow():
    keys = MagicMock()
    keys.__getitem__.side_effect = lambda k: k == pygame.K_RIGHT  # Only right arrow pressed
    strategy = NormalMovement()
    assert strategy.get_horizontal_velocity(3, keys) == 3


def test_normal_movement_right_d_key():
    keys = MagicMock()
    keys.__getitem__.side_effect = lambda k: k == pygame.K_d  # Only 'D' pressed
    strategy = NormalMovement()
    assert strategy.get_horizontal_velocity(9, keys) == 9


def test_normal_movement_no_keys_pressed():
    keys = MagicMock()
    keys.__getitem__.return_value = False  # No keys pressed
    strategy = NormalMovement()
    assert strategy.get_horizontal_velocity(10, keys) == 0


def test_no_movement_always_zero():
    keys = MagicMock()
    keys.__getitem__.return_value = True  # Even if keys are pressed
    strategy = NoMovement()
    assert strategy.get_horizontal_velocity(10, keys) == 0
    keys.__getitem__.return_value = False
    assert strategy.get_horizontal_velocity(5, keys) == 0
