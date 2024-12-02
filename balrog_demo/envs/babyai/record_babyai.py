from balrog_demo.cfg.arguments import parse_args, parse_full_cfg
from balrog_demo.cfg.cfg import add_extra_params_demo
from balrog_demo.envs.babyai.babyai_params import add_extra_params_babyai_env, babyai_override_defaults
from balrog_demo.play import play


def parse_babyai_args(argv=None):
    parser, partial_cfg = parse_args(argv=argv)
    add_extra_params_babyai_env(parser)
    add_extra_params_demo(parser)
    babyai_override_defaults(partial_cfg, parser)
    final_cfg = parse_full_cfg(parser, argv)
    return final_cfg


def main():
    cfg = parse_babyai_args()
    play(cfg)


if __name__ == "__main__":
    main()
