import ast

from balrog_demo.utils.utils import str2bool


def add_extra_params_pogs_env(parser):
    """
    Specify any additional command line arguments for NetHack environments.
    """
    # TODO: add help
    p = parser
    p.add_argument("--num_nodes", type=int, default=15)
    p.add_argument("--max_steps", type=int, default=30)
    p.add_argument("--k_nearest", type=int, default=3)
    p.add_argument("--min_backtracks", type=int, default=2)


def pogs_override_defaults(_env, parser):
    """RL params specific to pogs envs."""
    # set hyperparameter values to the same as in d&d
    parser.set_defaults(
        env="pogs",
    )
