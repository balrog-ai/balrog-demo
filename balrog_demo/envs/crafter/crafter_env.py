from pathlib import Path
from typing import Optional

import crafter
from balrog.environments.crafter import CrafterLanguageWrapper
from balrog.environments.env_wrapper import EnvWrapper
from balrog.environments.wrappers import GymV21CompatibilityV0

from balrog_demo.envs.crafter.play_wrapper import PlayCrafterWrapper
from balrog_demo.wrappers import PlayTextWrapper, Recorder


def make_crafter_env(env_name, task, config, render_mode: Optional[str] = None):
    render_mode = None if config.text_observation else render_mode

    crafter.constants.items["health"]["max"] = config.health
    crafter.constants.items["health"]["initial"] = config.health

    size = list(config.size)
    size[0] = size[0] or config.window[0]
    size[1] = size[1] or config.window[1]

    env = crafter.Env(area=config.area, size=size, view=config.view, length=config.length, seed=config.seed)
    env = CrafterLanguageWrapper(env, task, max_episode_steps=env._length)

    if not config.text_observation:
        env = PlayCrafterWrapper(env)

    env = GymV21CompatibilityV0(env=env, render_mode=render_mode)
    env = EnvWrapper(env, env_name, task)

    if config.text_observation:
        env = PlayTextWrapper(env)

    env = Recorder(env, Path(config.record) / env_name / task)

    return env
