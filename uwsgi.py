''' Run script for uwsgi '''

from index import app as application

if __name__ == "__main__":
    application.run()
