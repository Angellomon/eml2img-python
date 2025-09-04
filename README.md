# Eml2Img-python

> A tool to extract images from `.eml` files

## Usage

```bash
./eml2img.sh file.eml
```

Extracts the images from `file.eml` and creates a directory
with the same name where the images will be saved

---

```bash
./eml2img.sh --dir=files/
```

Extracts the images from a directory, it will scan all the `.eml` files inside.
The output files will be saved in the directory provided in directories named
after the `.eml` files.

---

```bash
./eml2img.sh file.eml --output=output-dir/
./eml2img.sh --dir=files --output=output-dir/
```

Will extract the images from the given files and save them in the `output-dir` directory
