#!/usr/bin/env python
from flask.ext.script import Manager

from apscheduler.scheduler import Scheduler
from common import data_ingestion
from common.models import User
from resources import app

manager = Manager(app)

@app.before_first_request
def init_scheduler():
    data_ingestion.insert_traffic_data()
    apsched = Scheduler()
    apsched.start()
    # Retrieve traffic data every 5 min
    apsched.add_interval_job(lambda: data_ingestion.insert_traffic_data(), seconds=300)


@manager.command
def adduser(username):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    user = User(username=username)
    user.set_password(password)
    user.save()
    print('User {0} was registered successfully.'.format(username))


@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage',
          '--cover-package=resources',
          '--cover-package=common' ])


if __name__ == '__main__':
    manager.run()

