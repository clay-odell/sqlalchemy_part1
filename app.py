"""Blogly application."""
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01302@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'mysuperdupersupersecretkey'
connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def users_list():
    users = User.query.all()
    return render_template('/users_list.html', users=users)

@app.route('/add_user_form', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        user_img_url = request.form['img-url']

        user = User(first_name=first_name, last_name=last_name, image_URL=user_img_url)
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    else:
        
        return render_template('add_user_form.html')
    

@app.route('/<user_id>')
def show_user(user_id):
    """Show Individual Users"""
    user = User.query.get_or_404(user_id)
    return render_template('/user_homepage.html', user=user)

@app.route('/<user_id>/edit_user_form', methods=['GET','POST'])
def edit_user(user_id):
    if request.method == 'POST':
        user = User.query.get(user_id)
        user.first_name = request.form['first-name']
        user.last_name = request.form['last-name']
        user.image_URL = request.form['img-url']
        db.session.commit()
        return redirect('/')

    else:
        user = User.query.get(user_id)
        return render_template('/edit_user_form.html', user=user)






