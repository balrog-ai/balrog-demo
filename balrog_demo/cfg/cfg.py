import ast
from argparse import ArgumentParser

from balrog_demo.utils.utils import str2bool


def add_basic_cli_args(p: ArgumentParser):
    p.add_argument("-h", "--help", action="store_true", help="Print the help message", required=False)
    p.add_argument("--env", type=str, default=None, help="Name of the environment to use", required=False)
    p.add_argument("--task", type=str, default=None, help="Name of the task to use", required=False)
    p.add_argument("--seed", type=int, default=None, help="Seed to use")


def add_default_env_args(p: ArgumentParser):
    p.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="Number of maximum steps per episode.",
    )
    p.add_argument(
        "--ngames",
        type=int,
        default=1,
        help="Number of episodes to play.",
    )
    p.add_argument(
        "--verbose",
        type=str2bool,
        default=False,
        help="Number of episodes to play.",
    )
    p.add_argument("--play-mode", type=str, default="human")
    p.add_argument("--no-render", action="store_true", help="Disables env.render().")
    p.add_argument(
        "--render_mode",
        type=str,
        default="human",
        choices=["human", "full", "ansi"],
        help="Render mode. Defaults to 'human'.",
    )


def add_extra_params_demo(parser: ArgumentParser):
    """ """
    p = parser
    p.add_argument(
        "--demodir",
        default="demo_data/play_data",
        type=str,
        help="Directory path where data will be saved. " "Defaults to 'demo_data/play_data'.",
    )
    p.add_argument("--demopath", default=None, type=str, help="If exists we will continue playing the demo from it.")
    p.add_argument(
        "--demostep", default=-1, type=int, help="If demopath exists we will continue playing the demo from this step."
    )
    p.add_argument("--save_every_k", default=100000, type=int, help="save checkpoint every kth step.")
    p.add_argument("--record", type=str, default=None)


def add_extra_params_replay(parser):
    p = parser
    p.add_argument(
        "--replay_path",
        type=str,
        default=None,
        help="Path to the demo file to replay",
    )
