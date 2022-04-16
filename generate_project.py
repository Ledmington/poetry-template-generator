import os

def generate_structure(proj_name):
    print("Generating structure...")

    main_dir = proj_name
    src_dir = main_dir + "/" + proj_name
    test_dir = main_dir + "/tests"

    os.mkdir(main_dir)
    open(main_dir+"/__init__.py", "w").close()
    os.mkdir(src_dir)
    open(src_dir+"/__init__.py", "w").close()
    with open(src_dir+"/main.py", "w") as f:
        f.write("def main():\n    print(\"Hello World\")")
        f.write("\n\nif __name__ == \"__main__\":\n    main()")
    os.mkdir(test_dir)
    open(test_dir+"/__init__.py", "w").close()
    with open(test_dir+"/test_"+proj_name+".py", "w") as f:
        f.write("def test_simple():\n    assert 2 == 2")

def generate_cov_config(proj_name):
    print("Generating coverage configuration...")
    with open("./.cov_config", "w") as f:
        f.write("[run]\n")
        f.write("omit =\n")
        f.write("    "+proj_name+"/tests/*\n")
        f.write("    **/__init__.py")

def generate_makefile(proj_name):
    print("Generating Makefile...")
    makefile = f"""RUN=poetry run

.PHONY: cov

update:
	poetry update
	poetry lock

install:
	poetry install

cov:
	${{RUN}} pytest --cov-config=.cov_config --cov-report html:cov_report --cov=./{proj_name} ./{proj_name}/tests

format:
	${{RUN}} black .

todo:
	find . | grep .py$$ | grep -rnw . -e TODO

clean:
	rm -rf cov_report dist .idea .ipynb_checkpoints
	rm -f .coverage*
	find ./ | grep __pycache__$ | xargs rm -rf
	find ./ | grep .pytest_cache$ | xargs rm -rf
"""
    with open("./Makefile", "w") as f:
        f.write(makefile)

def generate_poetry_dependencies(proj_name):
    print("Generating Poetry dependencies...")
    pyproject = f"""[tool.poetry]
name = "{proj_name}"
version = "0.1.0"
description = "Python-Poetry template"
authors = ["Ledmington <ledmington.dev@gmail.com>"]
\n
[tool.poetry.dependencies]
python = "^3.9"
\n
[tool.poetry.dev-dependencies]
pytest = "^7.1.1"
pytest-cov = "^3.0.0"
black = "^22.3.0"
\n
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""
    with open("./pyproject.toml", "w") as f:
        f.write(pyproject)

def generate_readme(proj_name):
    print("Generating README.md...")
    readme = f"# {proj_name}\n\n"
    """## Local development
    You need `poetry` installed to develop this software. You can install it with:
    ```
    pip install poetry
    ```
    After that, you can install the project dependencies with:
    ```
    make install
    ```"""
    with open("./README.md", "w") as f:
        f.write(readme)

def generate_git_stuff():
    print("Generating .gitignore and .gitattributes...")
    ignore = """cov_report/
.coverage*
**/.pytest_cache
**/__pycache__\n"""
    attributes = "* text=auto eol=lf\n"
    with open("./.gitignore", "w") as f:
        f.write(ignore)
    with open("./.gitattributes", "w") as f:
        f.write(attributes)

def generate_github_workflow(proj_name):
    print("Generating GitHub workflow...")
    workflow = f"""name: {proj_name} tests

on:
    workflow_dispatch:
    push:
        branches: [ master ]

jobs:
    tests:
    runs-on: ubuntu-latest
    strategy:
        matrix:
        pv: ['3.8', '3.9', '3.10']
    steps:
        - uses: actions/checkout@v2
        - uses: actions/setup-python@v2
        with:
            python-version: ${{{{ matrix.pv }}}}
            architecture: 'x64'
    
        - name: Install Poetry
        run: pip install poetry
    
        - name: Install dependencies
        run: make install
        
        - name: Tests
        run: make cov
"""
    os.mkdir(".github")
    os.mkdir(".github/workflows")
    with open(".github/workflows/test.yml", "w") as f:
        f.write(workflow)

def main():
    print("This a Poetry project template generator.")
    print("The folder where this script is is considered the new project folder.")

    proj_name = input("\nWhat is the name of the main package? ")

    generate_structure(proj_name)
    generate_cov_config(proj_name)
    generate_makefile(proj_name)
    generate_poetry_dependencies(proj_name)
    generate_readme(proj_name)
    generate_git_stuff()
    generate_github_workflow(proj_name)

    print("\nYour project is set up. You can now delete this script.")

if __name__ == "__main__":
    main()
