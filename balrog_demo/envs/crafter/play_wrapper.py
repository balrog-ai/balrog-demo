import gym
import pygame
from gym.utils.play import display_arr

# TODO: get them from the environment
keys_to_action = {
    (pygame.K_a,): "Move West",
    (pygame.K_d,): "Move East",
    (pygame.K_w,): "Move North",
    (pygame.K_s,): "Move South",
    (pygame.K_SPACE,): "Do",
    (pygame.K_TAB,): "Sleep",
    (pygame.K_r,): "Place Stone",
    (pygame.K_t,): "Place Table",
    (pygame.K_f,): "Place Furnace",
    (pygame.K_p,): "Place Plant",
    (pygame.K_1,): "Make Wood Pickaxe",
    (pygame.K_2,): "Make Stone Pickaxe",
    (pygame.K_3,): "Make Iron Pickaxe",
    (pygame.K_4,): "Make Wood Sword",
    (pygame.K_5,): "Make Stone Sword",
    (pygame.K_6,): "Make Iron Sword",
}


class PlayCrafterWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.current_seed = None

        self.video_size = None
        self.screen = None
        self.clock = pygame.time.Clock()
        self.fps = 30

        print("Actions:")
        for key, action in keys_to_action.items():
            print(f"  {pygame.key.name(key[0])}: {action}")

    def render(self, mode="human", **kwargs):
        if mode == "human":
            rendered = self.env.render(mode=None)

            if self.video_size is None:
                self.video_size = [rendered.shape[1], rendered.shape[0]]

            if self.screen is None:
                self.screen = pygame.display.set_mode(self.video_size)

            display_arr(self.screen, rendered, transpose=True, video_size=self.video_size)

            pygame.display.flip()
            self.clock.tick(self.fps)

    def close(self):
        if self.screen is not None:
            pygame.quit()
            self.screen = None

        return super().close()

    def get_action(self, env, play_mode, obs):
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
