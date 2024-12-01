import argparse
import glob
import os
import subprocess
from pathlib import Path


def main(args):
    env_dir = Path(args.replay_path) / args.env
    for entry in sorted(glob.glob(os.path.join(env_dir, "**/*.demo"), recursive=True)):
        task = "/".join(Path(entry).parents._parts[2:-1])
        seed = Path(entry).stem.split("_")[-1]
        command = [
            "python",
            "-m",
            f"balrog_demo.envs.{args.env}.replay_{args.env}",
            "--replay_path",
            args.replay_path,
            "--env",
            args.env,
            "--task",
            task,
            "--seed",
            seed,
            "--record",
            "records",
            "--no-render",
        ]
        if args.env == "nle" or args.env == "minihack":
            command.append("--vlm")
            command.append("True")
        subprocess.run(command, shell=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay_path", type=str, default=None, help="Path to the replay directory", required=True)
    parser.add_argument("--env", type=str, default=None, help="Name of the environment to use", required=True)
    args = parser.parse_args()
    main(args)
