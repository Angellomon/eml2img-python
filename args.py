import argparse

PROGRAM_NAME = "email2img"


class ArgParser:
    parser: argparse.ArgumentParser

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(prog=PROGRAM_NAME)
        self._setup_inputs()
        self._setup_output()

    def _setup_inputs(self):
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
            "-d",
            "--dir",
            nargs="?",
            const=".",
            default=None,
            help="specify a directory to parse, defaults to the current one",
        )

    def _setup_output(self):
        if not self.parser:
            return

        # optional output directory
        self.parser.add_argument(
            "-o",
            "--output",
            default=".",
            help="specify an output directory, defaults to the current one",
        )

    def parse_args(self):
        return self.parser.parse_args()
