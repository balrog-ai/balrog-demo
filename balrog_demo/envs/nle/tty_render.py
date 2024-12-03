import os

import gymnasium as gym
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class NLEImageTTYRender(gym.Wrapper):
    """
    A Gym environment wrapper for rendering TTY images in the NetHack Learning Environment (NLE).
    It overrides the obs["image"] which normally contains tiles based on glyphs
    """

    def __init__(self, env: gym.Env, image_size=(608, 432)):
        super().__init__(env)
        self.image_size = image_size

    def reset(self, **kwargs):
        obs, info = super().reset(**kwargs)
        obs["image"] = self.render_image(obs)

        return obs, info

    def step(self, action):
        obs, reward, terminated, truncated, info = super().step(action)
        obs["image"] = self.render_image(obs)

        return obs, reward, terminated, truncated, info

    def render_image(self, obs):
        obs = obs["obs"]
        tty_chars = obs["tty_chars"]
        tty_colors = obs["tty_colors"]
        tty_cursor = obs["tty_cursor"]
        image = tty_render(
            tty_chars, tty_colors, tty_cursor, font_path=os.path.join(os.path.dirname(__file__), "Hack-Regular.ttf")
        )
        image = image.resize(self.image_size)

        return image


def tty_render(chars, colors, cursor=None, font_size=16, font_path="Hack-Regular.ttf"):
    # Create font object
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

    height, width = chars.shape
    line_height = font_size + 6
    line_width = font_size - 6

    # Create image
    img = Image.new("RGB", (width * line_width, height * line_height), color="black")
    draw = ImageDraw.Draw(img)

    color_palette = [
        (0, 0, 0),
        (255, 0, 0),
        (0, 255, 0),
        (255, 255, 0),
        (0, 0, 255),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 255),
    ]

    color_palette = [
        # Standard colors (30-37)
        (0, 0, 0),  # Black
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (255, 255, 0),  # Yellow
        (0, 0, 255),  # Blue
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 255, 255),  # White
        # Bright colors (90-97)
        (128, 128, 128),  # Bright Black / Gray
        (255, 85, 85),  # Bright Red
        (85, 255, 85),  # Bright Green
        (255, 255, 85),  # Bright Yellow
        (85, 85, 255),  # Bright Blue
        (255, 85, 255),  # Bright Magenta
        (85, 255, 255),  # Bright Cyan
        (255, 255, 255),  # Bright White
    ]

    if cursor is None:
        cursor = (-1, -1)
    cursor = tuple(cursor)

    rows, cols = chars.shape
    y = 0
    for i in range(rows):
        x = 0
        for j in range(cols):
            draw.text((x, y), chr(chars[i, j]), fill=color_palette[colors[i, j] % 16], font=font)
            if cursor == (i, j):
                draw.text((x, y + 2), "_", fill=color_palette[7], font=font)

            x += line_width
        y += line_height

    return img
