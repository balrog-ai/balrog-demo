import ast

from balrog_demo.utils.utils import str2bool


def add_extra_params_nle_env(parser):
    """
    Specify any additional command line arguments for NetHack environments.
    """
    # TODO: add help
    p = parser
    p.add_argument("--character", type=str, default=None)
    p.add_argument("--max_episode_steps", type=int, default=None)
    p.add_argument("--penalty_step", type=float, default=-0.01)
    p.add_argument("--penalty_time", type=float, default=0.0)
    p.add_argument("--fn_penalty_step", type=str, default="constant")
    p.add_argument("--savedir", type=str, default=None)
    p.add_argument("--save_ttyrec_every", type=int, default=0)
    p.add_argument("--autopickup", type=str, default=None)
    p.add_argument("--vlm", type=str2bool, default=False)
    p.add_argument("--skip_more", type=str2bool, default=True)


def nle_override_defaults(_env, parser):
    """RL params specific to nle envs."""
    # set hyperparameter values to the same as in d&d
    parser.set_defaults(
        env="nle",
    )
