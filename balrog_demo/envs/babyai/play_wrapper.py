import gymnasium as gym
import pygame


class PlayBabyAIWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)

    def get_action(self, env, play_mode, obs):
        keys_to_action = {
            (pygame.K_UP,): "go forward",
            (pygame.K_LEFT,): "turn left",
            (pygame.K_RIGHT,): "turn right",
            (pygame.K_SPACE,): "toggle",
            (pygame.K_COMMA,): "pick up",
            (pygame.K_d,): "drop",
            (pygame.K_SEMICOLON,): "done",
        }
        relevant_keys = set(sum(map(list, keys_to_action.keys()), []))
        pressed_keys = []

        while True:
            # process pygame events
            for event in pygame.event.get():
                # test events, set key states
                if event.type == pygame.KEYDOWN:
                    if event.key in relevant_keys:
                        pressed_keys.append(event.key)
                elif event.type == pygame.QUIT:
                    return None

            action = keys_to_action.get(tuple(sorted(pressed_keys)), None)  # TODO: was 0
            pressed_keys = []

            if action is not None:
                return action

            env.render()
