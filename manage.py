from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app_instance, db

migrate = Migrate(app_instance, db)
manager = Manager(app_instance)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()