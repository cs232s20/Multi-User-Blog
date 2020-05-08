"""
The HTML forms for the blog are edited and modified using the template at
https://startbootstrap.com/themes/clean-blog/

The HTML form for the Sign-In, Sign-Out and Change Password were edited and
modified using the template at https://codepen.io/Devel0per95/pen/rjOpdx
"""

from flask import Flask, g, render_template, request, redirect, url_for, \
    jsonify, session
import os
from blog_db import BlogPost

app = Flask(__name__)
app.secret_key = 'generic_secret_key'
app.config['DATABASE'] = os.path.join(app.root_path, 'blog.sqlite')


def get_db():
    """
    Returns a BlogPost instance for accessing the database. If the database
    file does not yet exist, it creates a new database.
    """
    if not hasattr(g, 'blog_db'):
        g.blog_db = BlogPost(app.config['DATABASE'])

    return g.blog_db


@app.before_request
def before_request():
    """
    Changes user session every time user logs in.
    """
    g.user = None

    if 'user_id' in session:
        g.user = session['user_id']


@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Implements GET / or POST/. This is the default page whenever the default
    URL is used.

    :return: HTML page for login (GET). HTML page for index on successful
    login(POST).
    """
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        author_user = get_db().get_author_by_name(username)
        if author_user is not False:
            user = author_user['name']
            if get_db().password_check(user, password) is not False:
                session['user_id'] = user
                return redirect(url_for('index'))
            else:
                response = jsonify({'error': 'incorrect password'},
                                   {'status': 401})
                return response

        else:
            string = 'User named {} does not exist. Sign Up ' \
                     'if new user'.format(username)
            response = jsonify({'error': string}, {'status': 404})
            return response

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Implements GET /signup or POST/signup. This is the page for signing up
    new users.

    :return: HTML page for signup (GET). HTML page for login on successful
    login(POST).
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_db().sign_up_entry(username, password) is not False:
            return redirect(url_for('login'))
        else:
            return jsonify({'error': 'User already exists. Try signing in'},
                           {'status': 403})

    return render_template('signup.html')


@app.route('/change', methods=['GET', 'POST'])
def change():
    """
    Implements GET /change or POST/change. This is the page for changing
    password of existing user.

    :return: HTML page for change (GET). HTML page for login on successful
    password change(POST).
    """
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        old_password = request.form['old_password']
        if get_db().update_password(username, old_password, new_password) \
                is not False:
            return redirect(url_for('login'))
        else:
            response = jsonify({'error': 'Incorrect username or old_password'},
                               {'status': 401})
            return response

    return render_template('change.html')


@app.route('/index')
def index():
    """
    Implements GET /index. This is the home page for the blog

    :return: HTML page for index.
    """
    posts = get_db().get_all_posts()
    return render_template('index.html', posts=posts)


@app.route('/post/<post_id>')
def post(post_id):
    """
    Implements GET /post/:id

    :param post_id: id of the post
    :return: HTML of the specific post
    """
    to_post = get_db().get_blog_by_id(post_id)
    return render_template('post.html', post=to_post)


@app.route('/add')
def add():
    """
    Implements GET /add

    :return: HTML of the page where blog data is entered
    """
    return render_template('add.html')


@app.route('/addpost', methods=['POST'])
def addpost():
    """
    Implements POST /post

    Requires the blog-form parameters 'title', 'subtitle', and 'content'. The
    parameter for user name is a part of the user session.

    :return: HTML of the index after post has been made.
    """
    get_db().insert_blog(request.form['title'], request.form['subtitle'],
                         session['user_id'], request.form['content'])

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
