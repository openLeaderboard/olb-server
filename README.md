# olb-server
The backend for openLeaderboard

## Install

#### Requirements
* [poetry](https://python-poetry.org/docs/#installation)
* Python 3
* Docker
* pyenv

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

3. Setup pyenv to to use python 3.8+ in the olb-server directory

## Setup database
1. Install docker for your platform ([mac link](https://hub.docker.com/editions/community/docker-ce-desktop-mac))

2. Run the database (in the folder with manage.py)
```bash
docker-compose up
```

3. Create and upgrade the database
```bash
poetry run python manage.py reset_db
poetry run python manage.py db upgrade
```

## Run
1. Run the database (in the folder with manage.py)
```bash
docker-compose up
```

2. Run the server
```bash
poetry run python manage.py run
```

## Setup VSCode to use right environment
By default vscode will use your normal python install instead of the poetry virtual environment.
To fix this, launch vscode from within the poetry shell.
```bash
poetry shell
code .
```

Then select the poetry venv from the environment list on the bottom left.
