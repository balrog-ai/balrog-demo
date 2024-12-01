from balrog.environments.env_wrapper import EnvWrapper


def make_env(env_name, task, config, render_mode=None):
    """Create an environment instance with the appropriate wrapper based on the environment name.

    Args:
        env_name (str): The name of the environment to create.
        task (str): The specific task within the environment.
        config (dict): Configuration settings for the environment.
        render_mode (str, optional): Rendering mode for the environment. Defaults to None.

    Returns:
        EnvWrapper: A wrapped environment instance.

    Raises:
        ValueError: If the environment name is not recognized.
    """
    if env_name == "nle":
        from balrog_demo.envs.nle.nle_env import make_nle_env

        base_env = make_nle_env(env_name, task, config, render_mode=render_mode)
    elif env_name == "minihack":
        from balrog_demo.envs.minihack.minihack_env import make_minihack_env

        base_env = make_minihack_env(env_name, task, config, render_mode=render_mode)
    elif env_name == "babyai":
        from balrog_demo.envs.babyai.babyai_env import make_babyai_env

        base_env = make_babyai_env(env_name, task, config, render_mode=render_mode)
    elif env_name == "crafter":
        from balrog_demo.envs.crafter.crafter_env import make_crafter_env

        base_env = make_crafter_env(env_name, task, config, render_mode=render_mode)
    elif env_name == "textworld":
        from balrog_demo.envs.textworld.textworld_env import make_textworld_env

        base_env = make_textworld_env(env_name, task, config, render_mode=render_mode)
    elif env_name == "babaisai":
        from balrog_demo.envs.babaisai.babaisai_env import make_babaisai_env

        base_env = make_babaisai_env(env_name, task, config, render_mode=render_mode)
    else:
        raise ValueError(f"Unknown environment: {env_name}")
    return base_env
