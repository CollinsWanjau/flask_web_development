from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/about')
def about():
    return 'The About Page'

@app.route('/blog')
def blog():
    posts = [{'title': 'Technology in 2019', 'author':'Avi'},
            {'title': 'Expansion of oil in Russia', 'author':'Bob'}]
    return render_template('blog.html', author = "Bob", sunny=False, posts=posts)

@app.route('/blog/<string:blog_id>')
def blogpost(blog_id):
    return 'This is blog post number ' + blog_id

if __name__ == '__main__':
    app.run()
