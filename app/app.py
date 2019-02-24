from flask import Flask, render_template, session, redirect, url_for, session
import numpy as np
from flask_wtf import FlaskForm
from wtforms import (StringField, RadioField, DecimalField, SubmitField)
from wtforms.validators import DataRequired

from takeImage import takeImage
from face_comparison import intruder

import pickle

with open('data/user_pass.pkl', 'rb') as f:
    user_pass_df = pickle.load(f)

def confirm_login(username,password):

    final_dict = {}
    temp_list = []
    counter = 0

    result = user_pass_df.loc[(user_pass_df['user']==str(username)) & (user_pass_df['password']==str(password)),]
    if len(result) > 0:
        final_dict['valid'] = 1
    else:
        final_dict['valid'] = 0
    return final_dict

# we import the Twilio client from the dependency we just installed
from twilio.rest import Client

def send_sms():

    # the following line needs your Twilio Account SID and Auth Token
    client = Client("AC636b911804e4e5ece5bf99ff3a25c807", "f26bae5fde339ace48d8dda11cc830db")

    media_url = 'https://www.crosstimbersgazette.com/crosstimbersgazette/wp-content/uploads/2015/07/intruder.jpg'

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send SMS to any phone number
    client.messages.create(to="+16463513512", from_="+15167011855", body="INTRUDER ALERT!", media_url= media_url) # if you need to attach multimedia to your message, else remove this parameter.
    return (True)

app=Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):

    username = StringField("What is your username")
    password = StringField("What is your password")
    submit = SubmitField('Submit')

class DemosForm(FlaskForm):

    demo_selection = RadioField('Choose a demo', choices=[('intruder','intruder'),('baby','baby')])
    submit = SubmitField('Submit')

class TakeImageForm(FlaskForm):
    take_image_selection = RadioField('Take Image', choices=[('Yes','Yes'),('No','No')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    form = InfoForm()

    if form.validate_on_submit():

        # Grab the data from the breed on the form.
        session['Username'] = form.username.data;
        session['Password'] = form.password.data;

        results = confirm_login(session['Username'],session['Password'])
        print(results)

        if results['valid'] == 1:
            return redirect(url_for("main"))

    return render_template('index.html', form=form)

@app.route('/main', methods=['GET','POST'])
def main():

    demo_form = DemosForm()

    if demo_form.validate_on_submit():

        session['Demos Form'] = demo_form.demo_selection.data;

        if demo_form.demo_selection.data == 'intruder':
            return redirect(url_for("intruder_demo"))

    return render_template('main.html',demo_form=demo_form)

#First intruder alert page
@app.route('/intruder_demo', methods=['GET','POST'])
def intruder_demo():

    image_form = TakeImageForm()

    if image_form.validate_on_submit():

        session['Demos Form'] = image_form.take_image_selection.data;
        print(image_form.take_image_selection.data)

        if image_form.take_image_selection.data == 'Yes':
            takeImage()
            n_people, safe = intruder('data/image.png')
            print(n_people,safe)

            if safe == True:
                send_sms()
            #return redirect(url_for("intruder_results"))

    return render_template('intruder_demo.html',image_form=image_form)
'''
#Results page
@app.route('/intruder_demo', methods=['GET','POST'])
def intruder_results():
    n_people, safe = intruder('data/image.png')
    print(n_people,safe)
'''

if __name__ == "__main__":
    app.run(debug=True)
