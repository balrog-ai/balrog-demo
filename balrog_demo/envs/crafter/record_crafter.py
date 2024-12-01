import pygame

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


keys_to_action = {
    (pygame.K_a,): "Move West",
    (pygame.K_d,): "Move East",
    (pygame.K_w,): "Move North",
    (pygame.K_s,): "Move South",
    (pygame.K_SPACE,): "Do",
    (pygame.K_TAB,): "Sleep",
    (pygame.K_r,): "Place Stone",
    (pygame.K_t,): "Place Table",
    (pygame.K_f,): "Place Furnace",
    (pygame.K_p,): "Place Plant",
    (pygame.K_1,): "Make Wood Pickaxe",
    (pygame.K_2,): "Make Stone Pickaxe",
    (pygame.K_3,): "Make Iron Pickaxe",
    (pygame.K_4,): "Make Wood Sword",
    (pygame.K_5,): "Make Stone Sword",
    (pygame.K_6,): "Make Iron Sword",
}


def get_action(env, play_mode, obs):
    relevant_keys = set(sum(map(list, keys_to_action.keys()), []))
    pressed_keys = []

    while True:
        # process pygame events
        for event in pygame.event.get():
            # test events, set key states
            if event.type == pygame.KEYDOWN:
                if event.key in relevant_keys:
                    pressed_keys.append(event.key)
            elif event.type == pygame.QUIT:
                return None

        action = keys_to_action.get(tuple(sorted(pressed_keys)), None)  # TODO: was 0
        pressed_keys = []

        if action is not None:
            return action

        env.render()


def main():
    print("Actions:")
    for key, action in keys_to_action.items():
        print(f"  {pygame.key.name(key[0])}: {action}")

    cfg = parse_crafter_args()
    play(cfg, get_action=get_action)


if __name__ == "__main__":
    main()
