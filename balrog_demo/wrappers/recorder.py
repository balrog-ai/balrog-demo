# havily inspired by crafter recorder https://github.com/danijar/crafter/blob/main/crafter/recorder.py

import datetime
import json
import pathlib

import gymnasium as gym
import imageio
import numpy as np


class Recorder(gym.Wrapper):
    def __init__(self, env, directory, save_stats=True, save_video=True, save_episode=True, video_size=(512, 512)):
        if directory and save_stats:
            env = StatsRecorder(env, directory)
        if directory and save_video:
            env = VideoRecorder(env, directory, video_size)
        if directory and save_episode:
            env = EpisodeRecorder(env, directory)
        super().__init__(env)


class StatsRecorder(gym.Wrapper):
    def __init__(self, env, directory):
        super().__init__(env)
        self._directory = pathlib.Path(directory).expanduser()
        self._directory.mkdir(exist_ok=True, parents=True)
        self._file = (self._directory / "stats.jsonl").open("a")
        self._length = None
        self._reward = None
        self._unlocked = None
        self._stats = None

    def reset(self, **kwargs):
        obs, info = super().reset(**kwargs)
        self._length = 0
        self._reward = 0
        self._unlocked = None
        self._stats = None
        return obs, info

    def step(self, action):
        obs, reward, terminated, truncated, info = super().step(action)
        done = terminated or truncated
        self._length += 1
        self._reward += reward
        if done:
            self._stats = {"length": self._length, "reward": self._reward}
            self._save()
        return obs, reward, terminated, truncated, info

    def _save(self):
        self._file.write(json.dumps(self._stats) + "\n")
        self._file.flush()


class VideoRecorder(gym.Wrapper):
    def __init__(self, env, directory, size=(512, 512)):
        super().__init__(env)
        if not hasattr(env, "episode_name"):
            env = EpisodeName(env)
        self.env = env
        self._directory = pathlib.Path(directory).expanduser()
        self._directory.mkdir(exist_ok=True, parents=True)
        self._size = size
        self._frames = None

    def reset(self, **kwargs):
        obs, info = super().reset(**kwargs)
        self._frames = [obs["image"]]
        return obs, info

    def step(self, action):
        obs, reward, terminated, truncated, info = super().step(action)
        self._frames.append(obs["image"])
        if terminated or truncated:
            self._save()
        return obs, reward, terminated, truncated, info

    def _save(self):
        filename = str(self._directory / (self.env.episode_name + ".mp4"))
        imageio.mimsave(filename, self._frames)


class EpisodeRecorder(gym.Wrapper):
    def __init__(self, env, directory):
        super().__init__(env)
        if not hasattr(env, "episode_name"):
            env = EpisodeName(env)
        self.env = env
        self._directory = pathlib.Path(directory).expanduser()
        self._directory.mkdir(exist_ok=True, parents=True)
        self._episode = None

    def reset(self, **kwargs):
        obs, info = super().reset(**kwargs)
        transition = {**obs}
        self._episode = [transition]
        return obs, info

    def step(self, action):
        # Transitions are defined from the environment perspective, meaning that a
        # transition contains the action and the resulting reward and next
        # observation produced by the environment in response to said action.
        obs, reward, terminated, truncated, info = super().step(action)
        transition = {"action": action, **obs, "reward": reward, "terminated": terminated, "truncated": truncated}
        self._episode.append(transition)
        if terminated or truncated:
            self._save()
        return obs, reward, terminated, truncated, info

    def _save(self):
        filename = str(self._directory / (self.env.episode_name + ".npz"))
        # Fill in zeros for keys missing at the first time step.
        for key, value in self._episode[1].items():
            if key not in self._episode[0]:
                self._episode[0][key] = np.zeros_like(value)
        episode = {k: np.array([step[k] for step in self._episode]) for k in self._episode[0]}
        np.savez_compressed(filename, **episode)


class EpisodeName(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        self._timestamp = None
        self._unlocked = None
        self._seed = None
        self._length = 0
        self._reward = 0

    def reset(self, seed=None, **kwargs):
        self._seed = seed
        obs, info = super().reset(seed=seed, **kwargs)
        self._timestamp = None
        self._length = 0
        self._reward = 0
        return obs, info

    def step(self, action):
        obs, reward, terminated, truncated, info = super().step(action)
        self._length += 1
        self._reward += reward
        if terminated or truncated:
            self._timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
        return obs, reward, terminated, truncated, info

    @property
    def episode_name(self):
        return f"{self._timestamp}-seed{self._seed}-rew{self._reward:.2f}-len{self._length}"
