from pathlib import Path
from typing import Optional

import gym
import gym_battleship
from balrog.environments.battleships.base import BattleshipsWrapper
from balrog.environments.battleships.place_ship import PlaceShip
from balrog.environments.env_wrapper import EnvWrapper
from balrog.environments.wrappers import GymV21CompatibilityV0

from balrog_demo.envs.battleships.play_wrapper import PlayBattleshipsWrapper
from balrog_demo.wrappers import PlayTextWrapper, Recorder


def make_battleships_env(env_name, task, config, render_mode: Optional[str] = None):
    render_mode = None if config.text_observation else render_mode

    env_kwargs = dict(episode_steps=config.episode_steps)
    env = gym.make(task, **env_kwargs)
    env = PlaceShip(env)
    env = BattleshipsWrapper(env)
    env = PlayBattleshipsWrapper(env)

    env = GymV21CompatibilityV0(env=env, render_mode=render_mode)
    env = EnvWrapper(env, env_name, task)

    if config.text_observation:
        env = PlayTextWrapper(env)

    env = Recorder(env, Path(config.record) / env_name / task)

    return env
