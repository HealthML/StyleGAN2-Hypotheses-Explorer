#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path

from .logic.main import Main

if __name__ == '__main__':
    parser = ArgumentParser(
        description="StyleGAN2 Interactive WebClient server")
    parser.add_argument(
        "--export", help="Export the specified configuration for offline usage.", type=str)

    args = parser.parse_args()
    if args.export is None:
        Main().run()
    else:
        Main().export(Path(args.export))
