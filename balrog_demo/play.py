import pprint
import random
import timeit

import numpy as np

from balrog_demo.envs import make_env


def play(cfg):
    render_mode = cfg.render_mode
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
    action = None

    total_start_time = timeit.default_timer()
    start_time = total_start_time

    while True:
        action = env.get_wrapper_attr("get_action")(env, cfg.play_mode, obs)
        if action is None:
            break

        obs, reward, terminated, truncated, info = env.step(action)

        steps += 1
        total_reward += reward

        if not (terminated or truncated):
            continue

        time_delta = timeit.default_timer() - start_time

        if cfg.verbose:
            print("Final reward:", reward)
            print(f"Total reward: {total_reward}, Steps: {steps}, SPS: {steps / time_delta}", total_reward)
            pprint.pprint(info)

        break
    env.close()

    return info
