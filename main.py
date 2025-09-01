from args import ArgParser


def main():
    args_parser = ArgParser()
    args = args_parser.parse_args()

    filename: str = args.filename
    output_dir: str = args.output
    directory: str | None = args.dir

    print(f"{filename=}, {output_dir=}, {directory=}")


if __name__ == "__main__":
    main()
