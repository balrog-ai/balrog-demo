from pathlib import Path
from typing import Optional

import gym
import gym_pogs
from balrog.environments.env_wrapper import EnvWrapper
from balrog.environments.pogs.base import POGSWrapper
from balrog.environments.wrappers import GymV21CompatibilityV0

from balrog_demo.envs.pogs.play_wrapper import PlayPOGSWrapper
from balrog_demo.wrappers import PlayTextWrapper, Recorder


def make_pogs_env(env_name, task, config, render_mode: Optional[str] = None):
    render_mode = None if config.text_observation else render_mode

    env_kwargs = dict(
        num_nodes=config.num_nodes,
        episode_horizon=config.episode_horizon,
        k_nearest=config.k_nearest,
        min_distance=config.min_distance,
    )
    env = gym.make(task, **env_kwargs)
    env = POGSWrapper(env)
    env = PlayPOGSWrapper(env)

    env = GymV21CompatibilityV0(env=env, render_mode=render_mode)
    env = EnvWrapper(env, env_name, task)

    if config.text_observation:
        env = PlayTextWrapper(env)

    env = Recorder(env, Path(config.record) / env_name / task)

    return env
