import gymnasium as gym
import pygame


class PlayPOGSWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)

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
