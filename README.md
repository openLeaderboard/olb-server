# olb-server
The backend for openLeaderboard

## Install

#### Requirements
* [poetry](https://python-poetry.org/docs/#installation)
* Python 3
* Docker
* [pyenv](https://github.com/pyenv/pyenv-installer) (make sure you have ~/.zshrc and ~/.zsh_profile files or this will mess up on a mac install)

#### Steps
1. Clone the repo and open it
```bash
git clone https://github.com/openLeaderboard/olb-server.git
cd olb-server
```
2. Install python 3.8+ with pyenv
```
pyenv install -v 3.8.0
```

3a. Setup pyenv to to use python 3.8+ in the olb-server directory
```
pyenv local 3.8.0
```
3b. If this doesn't work, try setting it to the global version
```
pyenv global 3.8.0
```

4. Install the dependencies with poetry
```bash
poetry install
```



## Setup database
1. Install docker for your platform ([mac link](https://hub.docker.com/editions/community/docker-ce-desktop-mac))

2. Run the database (in the folder with manage.py)
```bash
docker-compose up
```

3. Create and upgrade the database (database must be running before you run these commands or they won't do anything)
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

**NOTE:** You will need to be running both of these simultaneously, use tmux or multiple terminals.

## Setup VSCode to use right environment
By default vscode will use your normal python install instead of the poetry virtual environment.
To fix this, launch vscode from within the poetry shell.
```bash
poetry shell
code .
```

Then select the poetry venv from the environment list on the bottom left.
