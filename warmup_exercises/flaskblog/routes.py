#im routes.py werden die verschiedenen Funktionen weitergeleitet

#Import allgemeine Betriebssystemfunktionalität
import os
#Generiert Nummern zur Verschleierung wichtiger Daten wie Passwörter
import secrets
#Import zum verkleiner der Profilbilder
from PIL import Image
#Import Flask
from flask import render_template, url_for, flash, redirect, request, abort
#Import der App sowie der Datenbank
from flaskblog import app, db
#Import der Funktion forms.py
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
#Import der Funktion models.py
from flaskblog.models import User, Post
#Import der Flask-Funktion login für die Benutzerverwaltung
from flask_login import login_user, current_user, logout_user, login_required

#Anzeigen aller Beiträge auf der Startseite
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

#Registierungsformular mit HTTP-Methode Get und Post
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        #falls angemeldet weiterleiten an die Startseite
        return redirect(url_for('home'))
    form = RegistrationForm()
    #Überprüfung der Daten beim Registierung
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        #Speicherung der Daten in der User-Datenbank.
        db.session.add(user)
        db.session.commit()
        #Anzeige bei erfolgreicher Anmeldung
        flash('Super, du hast jetzt einen Account und kannst dich einloggen', 'success')
        #Weiterleitung zum Login
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#Loginformular mit HTTP-Methode Get und Post
@app.route("/login", methods=['GET', 'POST'])
def login():
    #Falls Benutzer bereits angemeldet ist, weiterleiten zur Startseite
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    #Laden des Loginformulars
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            #Anzeige Fehlermeldung falls Login nicht funktioniert
            flash('Da passt was nicht, probiere es nochmals aus', 'danger')
    return render_template('login.html', title='Login', form=form)

#Einfaches Logout des Benutzers mit anschliessender Weiterleitung zur Startseite
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#Speicherung des Profilbildes
def save_picture(form_picture):
    #Umwandlung des Bildnamens in einen Token
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    #Anpassen der Grössen des Profilbildes welches hochgeladen wird
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#eigene Benutzerverwaltung mit Möglichkeit der Anpassung der Daten
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Deine Daten wurden aktualisiert', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

#Möglichkeit eine Beitrag hinzuzufügen, sofern man eingeloggt ist
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Dein Beitrag wurde gespeichert.', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

#Möglichkeit den eigenen Beitrag anzupassen
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    #Autor muss der eingeloggte Benutzer sein
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Dein Beitrag wurde aktualisiert', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

#Möglichkeit den eigenen Beitrag zu löschen
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Dein Beitrag wurde gelöscht. Mach doch gleich einen neuen!', 'success')
    return redirect(url_for('home'))