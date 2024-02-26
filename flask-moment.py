# FLASK-MOMENT
from flask import Flask, render_template
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
moment = Moment(app)

@app.route('/index')
def index():
    current_time = datetime.now()
    return render_template('index_1.html', current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)
