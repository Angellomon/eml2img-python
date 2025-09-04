import base64
import io
from pathlib import Path


class Eml2Img:
    _filename: Path | None = None
    _directory: Path | None = None
    _output_base: Path
    _output_dir: Path
    _is_default_output: bool

    def __init__(
        self, _filename: str | None, _directory: str | None = None, _output: str = "."
    ) -> None:
        if _filename is None:
            if _directory is None:
                raise ValueError("No filename or irectory where provided.")

            self._directory = self._resolve_path(_directory)
        else:
            self._filename = self._resolve_path(_filename)

        self._output_base = self._resolve_path(_output)
        self._output_dir = self._output_base
        self._is_default_output = _output == "."
        self._output_base.mkdir(exist_ok=True)

    def _resolve_path(self, path: str) -> Path:
        if path.startswith("~"):
            return Path(path).expanduser()

        if path.startswith("."):
            return Path(path).resolve()

        return Path(path)

    @property
    def is_dir(self) -> bool:
        return self._filename is None and self._directory is not None

    def _remove_path_extension(self, file: io.TextIOWrapper, sep: str = ".") -> str:
        return file.name.split(sep)[0]

    def _remove_file_extension(self, filename: str, sep: str = ".") -> str:
        return filename.split(sep)[0]

    def _get_last_part(self, file: io.TextIOWrapper) -> str:
        return Path(file.name).parts[-1]

    def _parse_file(self, file: io.TextIOWrapper):
        filename = self._get_last_part(file)
        filepath = self._remove_file_extension(filename)

        # if not self._output_base.name:
        #     self._output_dir = self._output_base.joinpath(filepath)
        if self.is_dir and self._is_default_output:
            assert self._directory is not None
            self._output_dir = self._directory.joinpath(filepath)
        # else:
        #     self._output_dir = self._output_base
        else:
            self._output_dir = self._output_base.joinpath(filepath)

        self._output_dir.mkdir(exist_ok=True)

        boundary = ""
        has_found_image = False
        is_reading_image_data = False
        image_name = ""
        image_content = ""

        image_types = ["jpeg", "jpg", "png"]

        CONTENT_TYPES_IMG = [
            f"Content-Type: image/{img_type};" for img_type in image_types
        ]

        CONTENT_TYPE_MULTIPART = "Content-Type: multipart/related;"

        for line in file:
            if CONTENT_TYPE_MULTIPART in line:
                boundary = self._extract_boundary(line)

                continue

            if any([content_type in line for content_type in CONTENT_TYPES_IMG]):
                image_name = self._extract_image_name(line)
                has_found_image = True
                is_reading_image_data = False
                image_content = ""

                continue

            # has found an image and the line is empty, next line starts the base64 data
            if has_found_image and len(line.split()) == 0:
                is_reading_image_data = True

                continue

            # is the end of image data
            if is_reading_image_data and line.startswith(boundary):
                self._save_image(image_name, image_content)

                has_found_image = False
                is_reading_image_data = False
                continue

            if is_reading_image_data:
                image_content += line

    def _extract_boundary(self, s: str) -> str:
        try:
            return "--" + s.split('boundary="')[1].split('"')[0]
        except IndexError:
            return ""

    def _extract_image_name(self, s: str) -> str:
        try:
            return s.split("; ")[1].split('"')[1]
        except IndexError:
            return ""

    def _parse_directory(self):
        if self._directory is None:
            return

        for file in self._directory.glob(r"**/*.eml"):
            with file.open("r") as _file:
                self._parse_file(_file)

    def _save_image(self, filename: str, content: str):
        try:
            path = self._output_dir.joinpath(filename)

            with path.open("wb") as img_file:
                img_file.write(base64.b64decode(content))
        except Exception as e:
            print(e)
            return

    def parse_eml(self):
        if self.is_dir or self._filename is None:
            self._parse_directory()

            return
        with self._filename.open("r") as file:
            self._parse_file(file)
