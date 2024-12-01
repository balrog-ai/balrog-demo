import ast

from balrog_demo.utils.utils import str2bool


def add_extra_params_babyai_env(parser):
    """
    Specify any additional command line arguments for NetHack environments.
    """
    # TODO: add help
    p = parser


def babyai_override_defaults(_env, parser):
    """RL params specific to Babaisai envs."""
    # set hyperparameter values to the same as in d&d
    parser.set_defaults(
        env="babyai",
    )
