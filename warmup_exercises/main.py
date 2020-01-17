#Die Funktionion sind in eigenen Packages gespeichert
#über die main.py wird die Flask-App geladen und weitergeleitet

from flaskblog import app

if __name__ == '__main__':
    app.run()