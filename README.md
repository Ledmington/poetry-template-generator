# poetry-template-generator
Generate simple Poetry projects in one click with this generator.

**IMPORTANT**: you need `python` and `poetry` installed to use this script.

## Instructions
Place this script inside the folder that will contain your project. Run:
```
python3 generate_project.py
```

The program will ask for the name of the main package and it will generate:
 - the main directory of the project divided into source and test subdirectories
 - the `pyproject.toml` poetry configuration file
 - a `.cov_config` pytest-cov configuration file
 - a simple `README.md`
 - a `Makefile` to make things even simpler
 - a `.gitignore` and a `.gitattributes`
 - a simple GitHub CI workflow

After the script has terminated, you can delete the script `generate_project.py` and start developing. Don't forget to `make install` before everything else, though.
