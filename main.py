from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///entries.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entries(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    truckno = db.Column(db.String(100), nullable=False)
    fromm = db.Column(db.String(100), nullable=False)
    to = db.Column(db.String(100), nullable=False)
    amt=db.Column(db.Integer, nullable=False)
    adv=db.Column(db.Integer, nullable=False)
    bal=db.Column(db.Integer, nullable=False)
    
    def __repr__(self)->str:
        return f"{self.sno}-{self.truckno}"

  
@app.route('/',methods=['GET','POST'])
def homepage():
    #THIS IS JUST A BASIC LOGIC
    if request.method=='POST':
        username=request.form['username']
        passw=request.form['pass']
        if username=='rohan' and passw=='11qq':

            return redirect("/test")
        else:
            return redirect("/")
    return render_template('login.html')


@app.route('/test', methods=['GET','POST'])
def test():
    if request.method=='POST':
       # submit=""
     #   search=""
        if request.form['submit']=='submit':
            truckno=request.form['truckno']
            fromm =request.form['fromm']
            to=request.form['to']
            amt=request.form['amt']
            adv=request.form['adv']
            bal=int(amt)-int(adv)
            entries=Entries(truckno=truckno,fromm=fromm,to=to,amt=amt,adv=adv,bal=bal)
            db.session.add(entries)
            db.session.commit()
        if request.form['submit']=='search':
            return redirect('/searchs')

        
    allentries= Entries.query.order_by(desc(Entries.date_created))
    #print(allentries)
    return render_template('test.html',allentries=allentries)


@app.route('/searchs', methods=['GET','POST'])
def search():
    search=""
    if request.method=='POST':
       search=request.form['search']
       
       entries=Entries.query.filter_by(truckno=search).all()
       
    allentries=Entries.query.filter_by(truckno=search).all()
    return render_template('searchs.html',allentries=allentries)



@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        truckno=request.form['truckno']
        fromm =request.form['fromm']
        to=request.form['to']
        amt=request.form['amt']
        adv=request.form['adv']
        
        entries=Entries.query.filter_by(sno=sno).first()
        entries.truckno=truckno
        entries.fromm=fromm
        entries.to=to
        entries.amt=amt
        entries.adv=adv
        entries.bal=int(entries.amt)-int(entries.adv)
        db.session.add(entries)
        db.session.commit()
        return redirect("/test")
    entries= Entries.query.filter_by(sno=sno).first()
    return render_template('update.html',entries=entries)


if __name__ == '__main__':
    app.run(debug=True)