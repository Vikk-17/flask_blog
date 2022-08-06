from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/blog_base" # mysql://username:password@server/db
db = SQLAlchemy(app)


class Contacts(db.Model):
    '''
    s_no, name, email, phone_number, message, date
    '''
    s_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/index')
# def index():
#     return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        data = request.form.to_dict()
        name = data['name']
        email = data['e_address']
        number = data['number']
        message = data['message']
        '''
        s_no, name, email, phone_number, message, date
        '''
        # print(name, email, number, message)
        entry = Contacts(name=name, email=email, phone_number=number, message=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('/contact.html')




@app.route('/post')
def post():
    return render_template('post.html')

