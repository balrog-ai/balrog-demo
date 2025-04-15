import sys

from balrog_demo.cfg.arguments import parse_args, parse_full_cfg
from balrog_demo.cfg.cfg import add_extra_params_demo
from balrog_demo.envs import get_env_config
from balrog_demo.play import play


def parse_env_args(env_name, argv=None):
    parser, partial_cfg = parse_args(argv=argv)
    param_adder, override_defaults = get_env_config(env_name)
    param_adder(parser)
    add_extra_params_demo(parser)
    override_defaults(partial_cfg, parser)
    final_cfg = parse_full_cfg(parser, argv)
    return final_cfg


def record(env_name, argv=None):
    cfg = parse_env_args(env_name, argv)
    play(cfg)


def main():
    env_name = sys.argv[2]
    argv = sys.argv[3:]
    record(env_name, argv=argv)


if __name__ == "__main__":
    main()
