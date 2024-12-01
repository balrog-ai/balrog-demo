import ast

from balrog_demo.utils.utils import str2bool


def add_extra_params_textworld_env(parser):
    """
    Specify any additional command line arguments for NetHack environments.
    """
    # TODO: add help
    p = parser
    p.add_argument("--objective", type=str2bool, default=True)
    p.add_argument("--description", type=str2bool, default=True)
    p.add_argument("--score", type=str2bool, default=True)
    p.add_argument("--max_score", type=str2bool, default=True)
    p.add_argument("--won", type=str2bool, default=True)
    p.add_argument("--max_episode_steps", type=int, default=80)
    p.add_argument("--textworld_games_path", type=str, default="tw_games")


def textworld_override_defaults(_env, parser):
    """RL params specific to Babaisai envs."""
    # set hyperparameter values to the same as in d&d
    parser.set_defaults(
        env="textworld",
        tasks=["treasure_hunter", "the_cooking_game", "coin_collector"],
    )
