from pathlib import Path
from typing import Optional

from baba import make
from balrog.environments.babaisai.base import BabaIsAIWrapper
from balrog.environments.env_wrapper import EnvWrapper
from balrog.environments.wrappers import GymV21CompatibilityV0

from balrog_demo.envs.babaisai.play_wrapper import PlayBabaisaiWrapper
from balrog_demo.wrappers import PlayTextWrapper, Recorder


def make_babaisai_env(env_name, task, config, render_mode: Optional[str] = None):
    render_mode = None if config.text_observation else render_mode

    env_kwargs = dict(add_ruleset=config.add_ruleset)
    env = make(task, **env_kwargs)
    env = BabaIsAIWrapper(env)

    if not config.text_observation:
        env = PlayBabaisaiWrapper(env)

    env = GymV21CompatibilityV0(env=env, render_mode=render_mode)
    env = EnvWrapper(env, env_name, task)

    if config.text_observation:
        env = PlayTextWrapper(env)

    env = Recorder(env, Path(config.record) / env_name / task)

    return env
