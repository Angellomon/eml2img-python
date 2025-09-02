from args import ArgParser
from converter import Eml2Img


def main():
    args_parser = ArgParser()
    args = args_parser.parse_args()

    filename: str = args.filename
    directory: str | None = args.dir
    output_dir: str = args.output

    converter = Eml2Img(filename, directory, output_dir)

    converter.parse_eml()

    print(f"{filename=}, {directory=}, {output_dir=}")


if __name__ == "__main__":
    main()
