import readline
from functools import partial

import gymnasium as gym


def completer(text, state, commands=[]):
    options = [cmd for cmd in commands if cmd.startswith(text)]
    return options[state] if state < len(options) else None


def setup_autocomplete(completer_fn):
    readline.parse_and_bind("tab: complete")
    print("Type commands and use TAB to autocomplete.")
    print("To see strategies use command: `help`")
    readline.set_completer(completer_fn)


class PlayTextWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.last_obs = None

    def system_prompt(self):
        instructions = None
        if self.env.env_name == "babyai":
            instructions = self.last_obs["mission"]
        return self.env.get_wrapper_attr("get_instruction_prompt")(instructions=instructions)

    def reset(self, **kwargs):
        obs, info = super().reset(**kwargs)
        self.last_obs = obs
        print(self.system_prompt())
        self.render()

        return obs, info

    def step(self, action):
        obs, reward, terminated, truncated, info = super().step(action)
        self.last_obs = obs
        self.render()

        return obs, reward, terminated, truncated, info

    def render(self, **kwargs):
        print(self.last_obs["text"]["long_term_context"])

    def get_action(self, env, play_mode, obs):
        language_action_space = self.env.get_wrapper_attr("language_action_space")
        setup_autocomplete(partial(completer, commands=language_action_space))

        while True:
            command = input("> ")

            if command == "help":
                print(language_action_space)
                continue
            else:
                try:
                    assert command in language_action_space
                    break
                except Exception:
                    print(f"Selected action '{command}' is not in action list. Please try again.")
                    continue

        return command
