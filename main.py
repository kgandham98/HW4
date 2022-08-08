import os
from flask import Flask, flash
from flask import Flask, render_template, request, redirect, session, url_for
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, BooleanField, RadioField, SelectField, TextAreaField, IntegerField
from wtforms import Form, BooleanField, StringField, PasswordField, validators, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder="./")
app.config['SECRET_KEY'] = 'HW04'
app. config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app. config[ 'SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class MyForm(FlaskForm):
    id_field = HiddenField()
    companyname = StringField('',validators=[DataRequired()], render_kw={"placeholder": "Enter Company Name"})
    email = StringField('',validators=[DataRequired()], render_kw={"placeholder": "Enter Email"})
    phonenum = IntegerField('',validators=[DataRequired()], render_kw={"placeholder": "Enter Phone Number"})
    address = StringField('',validators=[InputRequired()], render_kw={"placeholder": "Enter Address "})
    submit = SubmitField('Submit')
    
class UpdateForm(FlaskForm):
    id_field = HiddenField()
    companyname = StringField('',validators=[DataRequired()], render_kw={"placeholder": "Enter Company Name"})
    email = StringField('',validators=[DataRequired()], render_kw={"placeholder": "Enter Email"})
    phonenum = IntegerField('',validators=[DataRequired()], render_kw={"placeholder": "Enter Phone Number"})
    address = StringField('',validators=[InputRequired()], render_kw={"placeholder": "Enter Address "})   


@app.route('/addrecord', methods=['GET', 'POST'])
def addrecord():
    form = MyForm()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            companyname = request.form.get('companyname')
            email = request.form.get('email')
            phonenum = request.form.get('phonenum')
            address = request.form.get('address')
            new_company = yellowpages(companyname, email, phonenum, address)
            db.session.add_all([new_company])
            db.session.commit()
            return redirect(url_for('index'))   
    return render_template('addrecord.html', form = form)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'Search':
            search = request.form.get('phone')
            if search:
                print(search)
                search_record = yellowpages.query.filter_by(phonenum=search).all()
                print(search_record)
                if search_record:
                    return render_template('home.html', companydetails = search_record)           
        if request.form['submit'] == 'Add Record':
            return redirect(url_for('addrecord'))
        if request.form['submit'] == 'Delete Record':
            id = request.form.get('id')
            if id:
                #print(id)
                del_company = yellowpages.query.filter(yellowpages.id == id).first()
                db.session.delete(del_company)
                db.session.commit()
                return redirect(url_for('index'))
        if request.form['submit'] == 'Update Record':
            id = request.form.get('id')
            return redirect(url_for('updaterecord', a = id))
    companydetails = yellowpages.query.all()
    return render_template('home.html', companydetails = yellowpages.query.all())

 
@app.route('/updaterecord', methods=['GET', 'POST'])
def updaterecord():
    form = UpdateForm()
    a =request.args.get('a')
    print(a)
    if request.method == 'GET':
        if a:
            print('asda')
            return render_template('Update.html', form = form)
    elif request.method == 'POST':
        print('b')
        if a:
            if request.form['submit'] == 'Update':
                update_record = yellowpages.query.filter(yellowpages.id == a).first()
                #print(update_record)
                update_record.companyname = request.form.get('companyname')
                update_record.email = request.form.get('email')
                update_record.phonenum = request.form.get('phonenum')
                update_record.address = request.form.get('address')
                db.session.add(update_record)
                db.session.commit()
                return redirect(url_for('index'))
    return redirect(url_for('index'))         
    
class yellowpages(db.Model):
    __tablename__ = "yellowpages"

    id= db.Column(db.Integer, primary_key=True)
    companyname= db.Column(db.Text)
    email= db.Column(db.Text)
    phonenum= db.Column(db.Integer)
    address=db.Column(db.Text)

    def __init__ (self, companyname, email, phonenum, address):
        self.companyname=companyname
        self.email=email
        self.phonenum=phonenum
        self.address=address   
        
    def __repr__(self):
        return f'("{self.id}","{self.companyname}","{self.email}","{self.phonenum}","{self.address}")'    

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
#  References:
# 1. https://github.com/macloo/python-adv-web-apps/tree/master/python_code_examples/flask/databases
# 2. Source: Dr. Unan lecture, https://uab.instructure.com/courses/1576210/pages/week-07?module_item_id=16803884     
# 3. https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
# 4. Referred from previous Lab- 07, Lab- 08 and HW - 03
