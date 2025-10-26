# Development Environment Setup

This page contains information to set up the development environment.

## Pre-requisites

- Python 3.13+
- Poetry (for dependency management and installation)

## Install required tools

As per [PEP 668](https://peps.python.org/pep-0668/) starting with Python 3.12,
non-brew-packaged (macOS) Python package should only be installed in
virtual environments.

- Install python3 and pipx (macOS):

    ```shell
    # macOS commands.
    brew install python3
    brew install pipx
    ```

- Install python3 and pipx (Linux Ubuntu):

    ```shell
    # Ubuntu Linux commands.
    sudo apt update
    sudo apt install python3
    sudo apt install pipx
    ```

- Install several required utilities:

    ```shell
    pip install antlr4-python3-runtime
    pipx ensurepath
    pipx install fastmcp
    pipx install pylint
    pipx install pytest
    pipx install poetry
    pipx install python-semantic-release
    ```

- Upgrade above packages installed using `pipx`:

    ```shell
    pipx upgrade fastmcp
    pipx upgrade pylint
    pipx upgrade pytest
    pipx upgrade poetry
    ```

## Generate ANTLR4 Python Java 21+ Parsers

**NOTE**: This step had to be done at the beginning of the pojrect, and it
is no longer necessary. The Python Java 21+ Parser files are already stored in
the project's `src/javamcp/antlr4` folder. I have only included the below
instructions for reference, and in case I need to update the Java 21+ grammars.

1. Download Java 21+ grammars from [ANTLR Grammars](https://github.
   com/antlr/grammars-v4/tree/master/java/java) to the project `grammars`
   folder.
2. Then, run the `antlr4` parser generator.

   ```shell
   pushd grammars
   # Generate Python3 lexer and parser files into ../src/javamcp/antlr4
   antlr4 -Dlanguage=Python3 JavaLexer.g4 JavaParser.g4 -o ../src/javamcp/antlr4
   popd
   ```

## `poetry` dependencies

- Sample code to add dependencies to the `pyproject.toml`:

    ```shell
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
    cd $(git rev-parse --show-toplevel) || exit
    # to add runtime dependencies to pyproject.toml (e.g., fastmcp):
    poetry add fastmcp
    # to add development dependencies to pyproject.toml (e.g., coverage):
    poetry add --dev coverage
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

- To remove the virtual environment:

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
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
    cd $(git rev-parse --show-toplevel) || exit
    poetry run pylint "src" || {
     printf "failed pylint.\n" >&2
     sleep 120
     exit 1
    }
    ```

- Unit testing the project:

    ```shell
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
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
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
    cd $(git rev-parse --show-toplevel) || exit
    poetry run python -m coverage report -m
    ```

## Release process

### Prerequisites

Ensure the following tools are installed:

- gh version 2.81.0 or later (GitHub CLI tool)
- git version 2.43.0 or later

### Environment Variables

The release process is done on a Linux machine using a "Claude Code" custom
slash command `.claude/commands/release-plan.md`. Therefore, it is expected
that a `Claude Code` CLI session is started running on an underlying Linux
`bash` shell with the following environment variables set:

**Currently, only Rubens Gomes is able to push a release**

- GIT_AUTHOR_NAME
- GIT_AUTHOR_EMAIL
- GIT_COMMITTER_EMAIL
- GITHUB_USER
- GITHUB_TOKEN
- GH_TOKEN (should be same as GITHUB_TOKEN)

### Generating a release plan

The release plan is generated/executed within `Claude Code`. You must
start `Claude Code`, and run the following custom slash command:

- Claude code custom slash command:

    ```text
    /release-plan
    ```

- Then once the plan is reviewed and approved, you prompt `Claude Code` to
  proceed with the plan.

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
