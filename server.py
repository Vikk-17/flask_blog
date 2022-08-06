from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail


with open('config.json', 'r') as c:
    params = json.load(c)['params']

app = Flask(__name__)


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT="465",
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_password']
)
mail = Mail(app)

local_server = True
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else :
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

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
    return render_template('index.html', params=params)

# @app.route('/index')
# def index():
#     return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', params=params)


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
        
        mail.send_message("New message from " + name, 
        sender=email, 
        recipients=[params['gmail_user']],
        body=message + "\n" + number
        )

    return render_template('/contact.html', params=params)




@app.route('/post')
def post():
    return render_template('post.html', params=params)

