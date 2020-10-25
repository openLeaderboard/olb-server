import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import create_app, db, jwt
from app.main.models.db_models import blacklist_token, board_invite, board, match, user_board, user # noqa F401 -- needs to be here so manager will recognize changes for migrations
from app.main.services.auth_service import is_token_in_blacklist

from app import blueprint


app_env = os.getenv("OLB_ENV", "dev")  # set this environment variable, defaults to dev
app = create_app(app_env)
jwt.token_in_blacklist_loader(is_token_in_blacklist)
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)


# performs database migration
manager.add_command("db", MigrateCommand)


# runs the app
@manager.command
def run():
    print(f"Starting openLeaderboard api server in {app_env} mode")
    app.run()


# runs unit tests
@manager.command
def test():
    print("haha good joke")  # TODO: add some unit tests


if __name__ == "__main__":
    manager.run()
