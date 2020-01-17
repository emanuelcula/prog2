#Einstellung der Datenbank mit Inhalt welcher zur Verfügung gestellt werden soll

#Funktion zum Anzeigen der Zeit für generierte Beiträge
from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Datenbankeinstellung USER mit Parametern username, email, image_file, password und die erstellen Beiträge
class User(db.Model, UserMixin):
    #Einzigartige ID
    id = db.Column(db.Integer, primary_key=True)
    #Benutzername mit max. Länge von 20 Zeichen, muss einmalig sein und darf nicht leer sein
    username = db.Column(db.String(20), unique=True, nullable=False)
    #Email mit max. Länge von 50 Ziechen, muss einmalig sein und darf nicht leer sein
    email = db.Column(db.String(50), unique=True, nullable=False)
    #Profilbild welches falls leer ist das Default-Bild lädt.
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    #Passwort mit max. Länge von 60 Zeichen und darf nicht leer sein
    password = db.Column(db.String(60), nullable=False)
    #Post werden mit dem entsprechend Autor versehen
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

#Datenbankeinstellung POST mit Parameter title, Zeit, Inhalt und zum zuordner, die user_id
class Post(db.Model):
    #Einzigartige ID
    id = db.Column(db.Integer, primary_key=True)
    #Blogtitel mit max. Länge von 100 Zeichen und darf nicht leer sein
    title = db.Column(db.String(100), nullable=False)
    #Datum des erstellten Beitrages, genieriert mit dem Import datetime
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #Inhalt kann in ein Textfeld eingefügt werden
    content = db.Column(db.Text, nullable=False)
    #Post erhält die user_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"