import ast

from balrog_demo.utils.utils import str2bool


def add_extra_params_babaisai_env(parser):
    """
    Specify any additional command line arguments for NetHack environments.
    """
    # TODO: add help
    p = parser
    p.add_argument("--add_ruleset", type=str2bool, default=True)


def babaisai_override_defaults(_env, parser):
    """RL params specific to Babaisai envs."""
    # set hyperparameter values to the same as in d&d
    parser.set_defaults(
        env="babaisai",
    )
