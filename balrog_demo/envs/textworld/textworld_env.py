from pathlib import Path
from typing import Optional

from balrog.environments.env_wrapper import EnvWrapper
from balrog.environments.textworld import global_textworld_context
from balrog.environments.wrappers import GymV21CompatibilityV0

from balrog_demo.envs.textworld.play_wrapper import PlayTextWorldWrapper
from balrog_demo.wrappers import PlayTextWrapper, Recorder


def make_textworld_env(env_name, task, config, render_mode: Optional[str] = None):
    env_kwargs = dict(
        objective=config.objective,
        description=config.description,
        score=config.score,
        max_score=config.max_score,
        won=config.won,
        max_episode_steps=config.max_episode_steps,
        textworld_games_path=config.textworld_games_path,
    )
    textworold_context = global_textworld_context(tasks=config.tasks, **env_kwargs)
    env = textworold_context(task, seed=config.seed)

    if not config.text_observation:
        env = PlayTextWorldWrapper(env)

    env = GymV21CompatibilityV0(env=env, render_mode=render_mode)
    env = EnvWrapper(env, env_name, task)

    if config.text_observation:
        env = PlayTextWrapper(env)

    env = Recorder(env, Path(config.record) / env_name / task)

    return env
