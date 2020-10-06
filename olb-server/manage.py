import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api import create_app, db
from api.models import user # noqa F401 -- needs to be here so manager will recognize changes for migrations


app_env = os.getenv('OLB_ENV', 'dev')  # set this environment variable, defaults to dev
app = create_app(app_env)
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)


# performs database migration
manager.add_command('db', MigrateCommand)


# runs the app
@manager.command
def run():
    print(f'Starting openLeaderboard api server in {app_env} mode')
    app.run()


# runs unit tests
@manager.command
def test():
    print("haha good joke")  # TODO: add some unit tests


if __name__ == '__main__':
    manager.run()
