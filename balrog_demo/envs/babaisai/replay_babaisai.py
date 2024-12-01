from balrog_demo.cfg.arguments import parse_args, parse_full_cfg
from balrog_demo.cfg.cfg import add_extra_params_demo, add_extra_params_replay
from balrog_demo.envs.babaisai.babaisai_params import add_extra_params_babaisai_env, babaisai_override_defaults
from balrog_demo.legacy_replay import replay


def parse_babaisai_args(argv=None):
    parser, partial_cfg = parse_args(argv=argv)
    add_extra_params_babaisai_env(parser)
    add_extra_params_demo(parser)
    add_extra_params_replay(parser)
    babaisai_override_defaults(partial_cfg, parser)
    final_cfg = parse_full_cfg(parser, argv)
    return final_cfg


def main():
    cfg = parse_babaisai_args()
    replay(cfg)


if __name__ == "__main__":
    main()
