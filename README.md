# olb-server
The backend for openLeaderboard

## Install

#### Requirements
* [poetry](https://python-poetry.org/docs/#installation)
* Python 3

#### Steps
1. Clone the repo and open it
```bash
git clone https://github.com/openLeaderboard/olb-server.git
cd olb-server
```
2. Install the dependencies with poetry
```bash
poetry install
```

## Run
```bash
poetry run manager.py run_debug
```

## Setup VSCode to use right environment
By default vscode will use your normal python install instead of the poetry virtual environment.
To fix this, launch vscode from within the poetry shell.
```bash
poetry shell
code .
```

Then select the poetry venv from the environment list on the bottom left.
