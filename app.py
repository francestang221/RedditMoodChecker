from flask_login import LoginManager
import RedditScraper
import forms
import json
import models
import requests
from flask import Flask, g, render_template, flash, redirect, url_for

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'secret'

""" comment out for mvp deployment
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    #Connect to the database before each request
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    #Close the database connection after each request
    g.db.close()
    return response

"""

# Views


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        """
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        """
    return render_template('register.html', form=form)


# WIP
@app.route('/mood', methods=['GET', 'POST'])
def mood():
    form = forms.RedditForm()
    if form.validate_on_submit():
        subreddit = form.subreddit.data
        topic = form.topic.data
        # WIP: need to display in a scroll box
        data = RedditScraper.reddit_scraper(subreddit, topic)
        display_data = json.loads(data)['text']
        # get the mood result
        mood_url = "https://cs361-sentiment.herokuapp.com/tones"
        response = requests.post(mood_url, data=data)
        sentiments = json.loads(response.content)
        return render_template('mood.html', data=display_data, sentiments=sentiments, form=form)
    return render_template('mood.html', form=form)


@app.route('/searches')
def view_searches():
    return render_template('searches.html')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='frances',
            email='frances@goog.com',
            password='password',
            admin=True
        )
    except ValueError:
        pass
    app.run(DEBUG=DEBUG, host=HOST, port=PORT)
