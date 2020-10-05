from api import app
from flask_script import Manager

manager = Manager(app)


@manager.command
def run_debug():
    app.run(host="0.0.0.0", port=8888, debug=True)


if __name__ == '__main__':
    manager.run()
