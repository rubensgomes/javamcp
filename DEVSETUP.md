# Development Environment Setup

This page contains information to set up the development environment.

## Install required tools

As per [PEP 668](https://peps.python.org/pep-0668/) starting with Python 3.12,
non-brew-packaged (macOS) Python package should only be installed in
virtual environments.

- Commands to be used on a macOS (UNIX) machine:

    ```shell
    # macOS commands.
    brew install python3
    brew install pipx
    # Generic commands
    pip install antlr4-python3-runtime
    pipx ensurepath
    pipx install fastmcp
    pipx install pylint
    pipx install pytest
    pipx install poetry
    pipx install python-semantic-release
    ```

## `poetry` dependencies

- Sample code to add dependencies to the `pyproject.toml`:

    ```shell
    # to add runtime dependencies to pyproject.toml (e.g., fastmcp):
    # poetry add <pkg name>
    # to add development dependencies to pyproject.toml (e.g., coverage):
    # poetry add --dev <pkg name>
    ```

- Command to upgrade the packages in the `pyproject.toml`:

    ```shell
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
    cd $(git rev-parse --show-toplevel) || exit
    poetry update -vv
    poetry lock --regenerate -vv
    ```

## Python Virtual Environment

- Configure a local project virtual environment:

    ```shell
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
    cd $(git rev-parse --show-toplevel) || exit
    # Create virtual environment under <project>/.venv
    poetry config virtualenvs.in-project true
    # poetry automatically uses the existing virtual environment to install packages
    poetry install
    # display information about virtual environment 
    poetry env info
    poetry show
    ```

- Activate the virtual environment:

    ```shell
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
    cd $(git rev-parse --show-toplevel) || exit
    eval $(poetry env activate)
    poetry env activate
    ```

- To remove the virtual environment delete the `.venv` folder:

    ```shell
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
    cd $(git rev-parse --show-toplevel) || exit
    poetry env remove --all
    rm -fr .venv/
    ```

## Linting and Unit Testing

- Linting the project source code:

    ```shell
    cd $(git rev-parse --show-toplevel) || exit
    poetry run pylint "src" || {
     printf "failed pylint.\n" >&2
     sleep 120
     exit 1
    }
    ```

- Unit testing the project:

    ```shell
    cd $(git rev-parse --show-toplevel) || exit
    # run pytest with coverage
    poetry run python -m coverage run -m pytest tests/ || {
     printf "failed unit testing.\n" >&2
     sleep 10
     exit 1
    }
    ```

- Generate coverage report:

    ```shell
    cd $(git rev-parse --show-toplevel) || exit
    poetry run python -m coverage report -m
    ```

## Release process

### GH_TOKEN environment variable

A GH_TOKEN environment variable is required to create releases on GitHub.

### Generating a release plan

The release plan is generated/executed within `Claude Code`. You must 
start `Claude Code`, and run the following custom slash command:

- Claude code custom slash command:

    ```text
    /release-plan
    ```

## PyCharm IDE Development Environment

- First, ensure to follow all the previous steps to "Setting Up Shell
  Development Environment"

1. Open the project `java-mcp` folder using `PyCharm`
2. Follow instructions
   to [Create a Poetry environment](https://www.jetbrains.com/help/pycharm/poetry.html#poetry-env)
    - Click on the Python Interpreter Selector to "Add New Interpreter"
    - Select "Add Local Interpreter..."
    - Select "Poetry Environment"
    - Ensure "Base interpreter" is `/opt/homebrew/bin/python3` or
      `/usr/local/bin/python3` (macOS/Linux only)
    - Ensure "Poetry executable" (e.g., ${HOME}/.local/bin/poetry)
    - Click the OK button
3. Go to `PyCharm` > `Settings`
    - Enter `Python Integrated Tools`
    - Under `Testing` > `Default test runner` select `pytest`
4. Open `PyCharm` > `Terminal` to go to venv prompt
    - Ensure .venv correct settings:

    ```shell
    poetry env info
    ```
