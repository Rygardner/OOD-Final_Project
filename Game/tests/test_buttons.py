"""test_button.py

Tests for button.py
"""

import unittest
from unittest.mock import patch
from typing import Any
import pygame

from button import button


class TestButton(unittest.TestCase):
    """Tests for Button class
    """

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
    
    def test_init(self):
        """Button initializes with correct inputs
        """
        rect = pygame.Rect(10, 20, 100, 50)
        test_button = button(rect, "Play", (0, 0, 0), (255, 0, 0), 32)

        self.assertEqual(test_button.rect, rect)
        self.assertEqual(test_button.text, "Play")
        self.assertEqual(test_button.text_color, (0, 0, 0))
        self.assertEqual(test_button.color, (255, 0, 0))
        self.assertIsNotNone(test_button.font)

    def test_button_clicked_true(self):
        """button_clicked returns True when mouse is over the rect and pressed
        """
        rect = pygame.Rect(0, 0, 100, 100)
        test_button = button(rect, "Play", (0, 0, 0), (255, 0, 0), 32)

        with (
            patch("pygame.display.get_surface", return_value=object()),  # Don't display window
            patch("pygame.mouse.get_pos", return_value=(50, 50)),
            patch("pygame.mouse.get_pressed", return_value=(1, 0, 0))  # (left, middle, right)
        ):
            self.assertTrue(test_button.button_clicked())
    
    def test_button_clicked_false_no_display(self):
        """button_clicked returns False when no display surface exists
        """
        rect = pygame.Rect(10, 20, 100, 50)
        test_button = button(rect, "Play", (0, 0, 0), (255, 0, 0), 32)

        with patch("pygame.display.get_surface", return_value=None):
            self.assertFalse(test_button.button_clicked())

    def test_button_clicked_false_when_mouse_not_over_button(self):
        """button_clicked returns False when mouse is not inside the button rect
        """
        rect = pygame.Rect(0, 0, 100, 100)
        test_button = button(rect, "Play", (0, 0, 0), (255, 0, 0), 32)

        with (
            patch("pygame.display.get_surface", return_value=object()),
            patch("pygame.mouse.get_pos", return_value=(150, 150)),  # Mouse pos not over button
            patch("pygame.mouse.get_pressed", return_value=(1, 0, 0))  # Player clicks
        ):
            self.assertFalse(test_button.button_clicked())

    def test_draw_button_draws_rect_and_text(self):
        """draw_button draws the button rectangle and renders text onto the surface
        """
        rect = pygame.Rect(10, 20, 100, 50)
        test_button = button(rect, "Play", (0, 0, 0), (255, 0, 0), 32)

        surface = pygame.Surface((200, 200))

        with patch("pygame.draw.rect") as mock_rect:
            test_button.draw_button(surface)

        mock_rect.assert_called_once_with(surface, test_button.color, test_button.rect, border_radius=8)