from flask import Flask, escape, url_for, render_template
app = Flask(__name__)
"""
The render template integrates the Jinja2 template engine with the app.

Keywords args like name=name, the name on the left side represents the
arg name, which is used.

The name on the right is a variable in the current scope that provides
the value for the arg of the same name
"""


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return render_template('user.html', username=username)
    # return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

if __name__ == '__main__':
    app.run()
