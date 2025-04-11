from pathlib import Path
from typing import Optional

import gym_pogs
import gymnasium as gym
from balrog.environments.env_wrapper import EnvWrapper
from balrog.environments.pogs.base import POGSWrapper

from balrog_demo.envs.pogs.play_wrapper import PlayPOGSWrapper
from balrog_demo.wrappers import PlayTextWrapper, Recorder


def make_pogs_env(env_name, task, config, render_mode: Optional[str] = None):
    render_mode = None if config.text_observation else render_mode

    env_kwargs = dict(
        num_nodes=config.num_nodes,
        max_steps=config.max_steps,
        k_nearest=config.k_nearest,
        min_backtracks=config.min_backtracks,
    )
    env = gym.make(task, **env_kwargs, render_mode=render_mode)
    env = POGSWrapper(env)
    env = PlayPOGSWrapper(env)

    env = EnvWrapper(env, env_name, task)

    if config.text_observation:
        env = PlayTextWrapper(env)

    env = Recorder(env, Path(config.record) / env_name / task)

    return env
