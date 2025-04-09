import ast

from balrog_demo.utils.utils import str2bool


def add_extra_params_battleships_env(parser):
    """
    Specify any additional command line arguments for NetHack environments.
    """
    # TODO: add help
    p = parser
    p.add_argument("--episode_steps", type=int, default=50)


def battleships_override_defaults(_env, parser):
    """RL params specific to battleships envs."""
    # set hyperparameter values to the same as in d&d
    parser.set_defaults(
        env="battleships",
    )
