SUPPORTED_ENVS = ["nle", "minihack", "babyai", "crafter", "textworld", "babaisai", "battleships", "pogs"]


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
    if env_name not in SUPPORTED_ENVS:
        raise ValueError(f"Unknown environment: {env_name}")

    # Dynamically import the appropriate module and call the make_env function
    module = __import__(f"balrog_demo.envs.{env_name}.{env_name}_env", fromlist=[f"make_{env_name}_env"])
    make_env_func = getattr(module, f"make_{env_name}_env")

    return make_env_func(env_name, task, config, render_mode=render_mode)


def get_env_config(env_name: str):
    if env_name not in SUPPORTED_ENVS:
        raise ValueError(f"Unknown environment: {env_name}")

    module = __import__(
        f"balrog_demo.envs.{env_name}.{env_name}_params",
        fromlist=[f"add_extra_params_{env_name}_env", f"{env_name}_override_defaults"],
    )
    param_adder = getattr(module, f"add_extra_params_{env_name}_env")
    override_defaults = getattr(module, f"{env_name}_override_defaults")

    return param_adder, override_defaults
