from flask import Flask, render_template

app = Flask(__name__)

posts = [
	{
		'author': 'Emanuel Cula',
		'title': 'Übung 1',
		'content': 'Erster Beitrag',
		'date_posted': '1. Januar 2020'
	},
	{
		'author': 'Cula Emanuel',
		'title': 'Übung 2',
		'content': 'Zweiter Beitrag',
		'date_posted': '2. Januar 2020'
	}
]


@app.route("/")
@app.route("/home")
def home():
	return render_template('index.html', posts=posts)


@app.route("/kontakt")
def about():
	return render_template ('kontakt.html', title='Kontakt')


if __name__ == '__main__':
	app.run()