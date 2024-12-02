import gym


class PlayTextWorldWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)

    def get_action(self, env, mode, typing):
        command = input("> ")
        return command
