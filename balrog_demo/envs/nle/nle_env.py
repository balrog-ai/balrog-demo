from pathlib import Path
from typing import Optional

import gym
import nle  # NOQA: F401
from balrog.environments.env_wrapper import EnvWrapper
from balrog.environments.nle import NLELanguageWrapper
from balrog.environments.wrappers import GymV21CompatibilityV0

from balrog_demo.envs.nle.play_wrapper import PlayNLEWrapper
from balrog_demo.wrappers import PlayTextWrapper, Recorder

NETHACK_ENVS = []
for env_spec in gym.envs.registry.all():
    id = env_spec.id
    if id.split("-")[0] == "NetHack":
        NETHACK_ENVS.append(id)


def make_nle_env(env_name, task, config, render_mode: Optional[str] = None):
    render_mode = None if config.text_observation else render_mode

    observation_keys = (
        "glyphs",
        "blstats",
        "tty_chars",
        "inv_letters",
        "inv_strs",
        "tty_cursor",
        "tty_colors",
    )

    kwargs = dict(
        observation_keys=observation_keys,
        penalty_step=config.penalty_step,
        penalty_time=config.penalty_time,
        penalty_mode=config.fn_penalty_step,
        savedir=config.savedir,
        save_ttyrec_every=config.save_ttyrec_every,
    )

    if config.character is not None:
        kwargs["character"] = config.character

    if config.max_episode_steps is not None:
        kwargs["max_episode_steps"] = config.max_episode_steps

    if config.autopickup is not None:
        kwargs["autopickup"] = config.autopickup

    env = gym.make(task, **kwargs)
    env = NLELanguageWrapper(env, vlm=config.vlm, skip_more=config.skip_more)

    if not config.text_observation:
        env = PlayNLEWrapper(env)

    env = GymV21CompatibilityV0(env=env, render_mode=render_mode)
    env = EnvWrapper(env, env_name, task)

    if config.text_observation:
        env = PlayTextWrapper(env)
    env = Recorder(env, Path(config.record) / env_name / task)

    return env
