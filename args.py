import argparse

PROGRAM_NAME = "email2img"


class ArgParser:
    parser: argparse.ArgumentParser

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(prog=PROGRAM_NAME)
        self._setup_args()

    def _setup_args(self):
        if not self.parser:
            return

        # mutually excluseive arguments, at least one required
        group = self.parser.add_mutually_exclusive_group(required=True)

        # single file argument, non positional
        group.add_argument(
            "filename", nargs="?", help="specify the .eml file to extract the images"
        )

        # directory flag argument, non positional
        group.add_argument(
            "--dir",
            nargs="?",
            const=".",
            default=None,
            help="specify a directory to parse, defaults to the current one",
        )

        # optional output directory
        group.add_argument(
            "-o",
            "--output",
            nargs="?",
            default=".",
            help="specify an output directory, defaults to the current one",
        )
