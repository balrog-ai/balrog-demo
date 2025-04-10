import gym
import pygame
from gym.utils.play import display_arr


class PlayPOGSWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)

        self.video_size = None
        self.screen = None
        self.clock = pygame.time.Clock()
        self.fps = 30

    def render(self, mode="human", **kwargs):
        if mode == "human":
            rendered = self.env.render()

            if self.video_size is None:
                self.video_size = [rendered.shape[1], rendered.shape[0]]

            if self.screen is None:
                self.screen = pygame.display.set_mode(self.video_size)

            display_arr(self.screen, rendered, transpose=True, video_size=self.video_size)

            pygame.display.flip()
            self.clock.tick(self.fps)
        else:
            return self.env.render(mode=mode, **kwargs)

    def close(self):
        if self.screen is not None:
            pygame.quit()
            self.screen = None

        return super().close()

    def get_action(self, env, mode, typing):
        action = ""
        submit_text = False

        # Initialize a list to store pressed keys
        pressed_keys = []

        # Define relevant keys if not defined elsewhere
        relevant_keys = [pygame.K_RETURN, pygame.K_BACKSPACE] + [
            getattr(pygame, f"K_{chr(i)}") for i in range(32, 127) if hasattr(pygame, f"K_{chr(i)}")
        ]

        while True:
            # Process pygame events
            for event in pygame.event.get():
                # Handle key events
                if event.type == pygame.KEYDOWN:
                    if event.key in relevant_keys:
                        pressed_keys.append(event.key)

                    # Handle text input within the KEYDOWN event
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        submit_text = True
                    elif event.key == pygame.K_BACKSPACE:
                        action = action[:-1]
                    else:
                        action += event.unicode

                if event.type == pygame.QUIT:
                    return None

            env.render()

            if submit_text:
                return action

            # Add a small delay to prevent high CPU usage
            pygame.time.delay(10)
