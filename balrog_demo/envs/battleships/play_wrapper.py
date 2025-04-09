import gym


class PlayBattleshipsWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)

    def get_action(self, env, mode, typing):
        command = input("> ")
        return command

    def render(self, mode="human", **kwargs):
        text_observation = self.get_text_observation(self.env.observation)
        print(text_observation)
