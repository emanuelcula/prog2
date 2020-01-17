#Import Modul für Formulare und Login
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#Import der User aus models.py
from flaskblog.models import User

#Formular Registrierung neuer Benutzer
class RegistrationForm(FlaskForm):
    username = StringField('Benutzername',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    confirm_password = PasswordField('Bestätige das Passwort',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Jetzt Registrieren')

    #Kontrolle ob Username und Email bereits in der Datenbank sind.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Sorry, der Benutzer ist bereits vergeben.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Sorry, diese E-Mail ist bereits vergeben.')

#Login-Formular für bereits registrierte Benutzer. Anmeldung via Email und Passwort
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember = BooleanField('Passwort merken')
    submit = SubmitField('Anmelden')

#Funktion um Benutzerinfos zu aktualisieren
class UpdateAccountForm(FlaskForm):
    username = StringField('Benutzername',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profilbild', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    #Kontrolle ob neuer Benutzername bereits vergeben ist
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Sorry, den gibts schon, wähle eine neuen Benutzernamen aus')

    #Kontrolle ob neue Email bereits vergeben ist
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Sorry, die E-Mail verwendet bereits jemand')

#Formular zum Beiträge veröffentlich. Fragt benötigte Daten für die Datenbank ab.
class PostForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired()])
    content = TextAreaField('Beitrag', validators=[DataRequired()])
    submit = SubmitField('Veröffentlichen')