# Development Environment Setup

This page contains information to set up the development environment.

## Install required tools

- pyenv 2.6+
- python 3.14+
- pipx 1.4+
- Poetry 2.2+

### `pyenv`

- Install `pyenv` as follows:

    ```bash
    mkdir -p "${HOME}/tmp"
    cd "${HOME}/tmp"
    git clone https://github.com/pyenv/pyenv.git
    sudo rm -rf /opt/pyenv
    sudo mv pyenv /opt/pyenv
    ```

- Ensure you add the `/opt/yenv/bin` to your environment PATH variable

    ```bash
    export PATH="${PATH}:/opt/pyenv/bin"
    ```

### `python`

- Grabs the latest `python` 3.14 version as follows:

    ```bash
    pyenv install --list | grep '^[[:space:]]*3.14'
    ```

- Install `python` 3.14 as follows:

    ```bash
    # assuming 3.14.2 is the latest python 3.14 release.
    pyenv install "3.14.2"
    ```

- Configure the `python` global:

    ```bash
    # assuming 3.14.2 is the latest python 3.14 release.
    pyenv globa "3.14.2"
    ```

- Check `python` version installed:

    ```bash
    python --version
    ```

### `pipx`

- Install python3 and pipx (macOS):

    ```bash
    # macOS brew
    brew install pipx
    pipx ensurepath
    ```

- Install python3 and pipx (Linux Ubuntu using `apt`):

    ```bash
    # Ubuntu Linux apt.
    sudo apt update
    sudo apt install pipx
    pipx ensurepath
    ```

- Check `pipx` version installed:

    ```bash
    pipx --version
    ```
  
### `poetry` `pylint` `pytest`
- 

- Install several required utilities:

    ```bash
    pipx install poetry
    pipx install pylint
    pipx install pytest
    ```
- Upgrade above packages installed using `pipx`:

    ```bash
    pipx upgrade poetry
    pipx upgrade pylint
    pipx upgrade pytest
    ```

- Check `poetry` version installed:

    ```bash
    poetry --version
    ```

- Check `pylint` version installed:

    ```bash
    pylint --version
    ```

- Check `pytest` version installed:

    ```bash
    pytest --version
    ```

## Generate ANTLR4 Python Java 21+ Parsers

**NOTE**: This step had to be done at the beginning of the project, and it
is no longer necessary. The Python Java 21+ Parser files are already stored in
the project's `src/javamcp/antlr4` folder. I have only included the below
instructions for reference, and in case I need to update the Java 21+ grammars.

1. Download the following Java 21+ grammars files from
   [ANTLR Grammars](https://github.com/antlr/grammars-v4/tree/master/java/java)
   to the project `grammars` folder:

    - JavaLexer.g4
    - JavaParser.g4

2. Install `antlr4-python3-runtime` and `antlr4-tools`:

    ```bash
    pip install antlr4-tools
    ```

3. Then, run the `antlr4` parser generator.

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    pushd grammars
    # Generate Python3 lexer and parser files into ../src/javamcp/antlr4
    antlr4 -Dlanguage=Python3 -visitor -o ../src/javamcp/antlr4 JavaLexer.g4 JavaParser.g4 
    popd
    ```

4. Install the matching `antlr4-python3-runtime` version:
    ```bash
   # check the version of antlr4 (e.g., ANTLR Parser Generator  Version 4.13.2)
   antlr4
   # install the same version of antlr4-python3-runtime
   pip install "antlr4-python3-runtime==4.13.2"
   ```

## Python `poetry` commands

- Sample code to add dependencies to the `pyproject.toml`:

    ```bash
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
    cd $(git rev-parse --show-toplevel) || exit
    # to add runtime dependencies to pyproject.toml (e.g., fastmcp):
    poetry add fastmcp
    # to add development dependencies to pyproject.toml (e.g., coverage):
    poetry add --dev coverage
    ```

- Command to upgrade the packages in the `pyproject.toml`:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    poetry update -vv
    poetry lock --regenerate -vv
    ```

## Python Virtual Environment

- Configure a local project virtual environment:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    # poetry automatically uses the existing virtual environment to install packages
    poetry install
    # display information about virtual environment 
    poetry env info
    poetry show
    ```

- Activate the virtual environment:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    eval $(poetry env activate)
    ```

- De-activate the virtual environment:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    deactivate
    ```

- To remove the virtual environment:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    poetry env remove --all
    ```

## Linting and Unit Testing

- Linting the project source code:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    poetry run pylint \
      --ignore=src/javamcp/antlr4 \
      --ignore-paths='^.*/antlr4/.*' \
      "src/javamcp"
    ```

- Unit testing the project:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    # run pytest with coverage
    poetry run python -m coverage run -m pytest tests/
    ```

- Generate coverage report:

    ```shell
    # Ensure at the top of the project root folder
    # NOTE: this assumes you have cloned this project from a Git repo
    cd $(git rev-parse --show-toplevel) || exit
    poetry run python -m coverage report -m
    ```

## Installing and Running `Claude Code`

- Install `Claude Code`:

    ```bash
    curl -fsSL https://claude.ai/install.sh | bash
    ```

- Clean cache of any previous stale `Claude Code` installation:

    ```bash
    hash -d claude   # clears cached location for 'claude' only
    # if it says 'not found', just run:
    hash -r          # clears the whole cache
    ```

- Display `Claude Code` version and help:

    ```bash
    claude --version
    claude --help
    ```

- Update `Claude Code`:

    ```bash
    claude update
    ```

- Run `Claude Code` using latest `opus` LLM:

    ```bash
    # switch to project folder, and type:
    claude --verbose --debug --model "opus" --ide
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
    /release-plan javamcp
    ```

- Then once the plan is reviewed and approved, you prompt `Claude Code` to
  proceed with the plan.

## PyCharm IDE Development Environment

- First, ensure to follow all the previous steps to "Setting Up Shell
  Development Environment"

1. Open the project `javamcp` folder using `PyCharm`
2. Follow instructions
   to [Create a Poetry environment](https://www.jetbrains.com/help/pycharm/poetry.html#poetry-env)
    - Click on the Python Interpreter Selector to "Add New Interpreter"
    - Select "Add Local Interpreter..."
    - Select "Poetry Environment"
    - Ensure "Poetry executable" (e.g., ${HOME}/.local/bin/poetry)
    - Ensure "Base interpreter" is `poeetry` and the right Python executable.
    - Enter `Python Integrated Tools`
    - Under `Testing` > `Default test runner` select `pytest`
3. Open `PyCharm` > `Terminal` to go to venv prompt
    - Ensure .venv correct settings:

    ```shell
    poetry env info
    ```
