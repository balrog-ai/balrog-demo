from balrog_demo.cfg.arguments import parse_args, parse_full_cfg
from balrog_demo.cfg.cfg import add_extra_params_demo
from balrog_demo.envs.crafter.crafter_params import add_extra_params_crafter_env, crafter_override_defaults
from balrog_demo.play import play


def parse_crafter_args(argv=None):
    parser, partial_cfg = parse_args(argv=argv)
    add_extra_params_crafter_env(parser)
    add_extra_params_demo(parser)
    crafter_override_defaults(partial_cfg, parser)
    final_cfg = parse_full_cfg(parser, argv)
    return final_cfg


def main():
    cfg = parse_crafter_args()
    play(cfg)


if __name__ == "__main__":
    main()
