import pickle
import random
import timeit
from pathlib import Path

import numpy as np

from balrog_demo.envs import make_env


def replay(cfg):
    render_mode = "human"
    if cfg.no_render:
        render_mode = None

    env = make_env(cfg.env, cfg.task, cfg, render_mode=render_mode)

    if cfg.seed is not None:
        np.random.seed(cfg.seed)
        random.seed(cfg.seed)
    obs, info = env.reset(seed=cfg.seed)

    steps = 0
    reward = 0.0
    total_reward = 0.0

    total_start_time = timeit.default_timer()
    start_time = total_start_time

    savedir = Path(cfg.replay_path) / cfg.env / cfg.task
    game_name = f"seed_{cfg.seed}"
    paths = [path.stem for path in savedir.iterdir() if game_name in path.stem]
    if paths:
        game_name = paths[0]
    game_path = Path(savedir) / f"{game_name}.demo"

    with open(game_path, "rb") as f:
        data = pickle.load(f)

    recorded_actions = data["actions"]
    recorded_rewards = data["rewards"]

    for i, (recorded_action, recorded_reward) in enumerate(zip(recorded_actions, recorded_rewards)):
        obs, reward, terminated, truncated, info = env.step(env.get_wrapper_attr("get_text_action")(recorded_action))
        # assert reward == recorded_reward
        steps += 1
        total_reward += reward

        if not (terminated or truncated):
            continue

        time_delta = timeit.default_timer() - start_time

        if cfg.verbose:
            print("Final reward:", reward)
            print("End status:", info.get("end_status", ""))
            print(f"Total reward: {total_reward}, Steps: {steps}, SPS: {steps / time_delta}", total_reward)

        break

    env.close()

    return info
