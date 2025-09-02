import base64
import io
from pathlib import Path


class Eml2Img:
    _filename: Path
    _directory: Path | None
    _output: Path

    is_dir: bool

    def __init__(
        self, _filename: str, _directory: str | None = None, _output: str = "."
    ) -> None:
        self._filename = Path(_filename)
        self._directory = Path(_directory) if _directory else None
        self._output = Path(_output)

        self.is_dir = self._directory is not None

    def _remove_extension(self, file: io.TextIOWrapper, sep: str = ".") -> str:
        return file.name.split(sep)[0]

    def _parse_file(self, file: io.TextIOWrapper):
        if not self._output.name:
            name = self._remove_extension(file)
            self._output = self._output.joinpath(name)

        self._output.mkdir(exist_ok=True)

        boundary = ""
        has_found_image = False
        is_reading_image_data = False
        image_name = ""
        image_content = ""

        CONTENT_TYPE_IMG_JPEG = "Content-Type: image/jpeg;"
        CONTENT_TYPE_IMG_JPG = "Content-Type: image/jpg;"
        CONTENT_TYPE_IMG_PNG = "Content-Type: image/png;"

        CONTENT_TYPES_IMG = [
            CONTENT_TYPE_IMG_JPEG,
            CONTENT_TYPE_IMG_JPG,
            CONTENT_TYPE_IMG_PNG,
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

        for file in self._directory.glob("**/*.eml"):
            with file.open("r") as _file:
                self._parse_file(_file)

    def _save_image(self, filename: str, content: str):
        try:
            path = self._output.joinpath(filename)

            with path.open("wb") as img_file:
                img_file.write(base64.b64decode(content))
        except Exception:
            return

    def parse_eml(self):
        if self.is_dir:
            self._parse_directory()

            return

        with self._filename.open("r") as file:
            self._parse_file(file)
