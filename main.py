from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc 
import xlrd as xl   
from decimal import Decimal
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///entries.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
key=""
class Entries(db.Model):
    party=db.Column(db.String(100), nullable=False)
    sno = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.String(10),nullable=False)
    truckno = db.Column(db.String(100), nullable=False)
    cweight=db.Column(db.Numeric(10,3), nullable=False)
    rweight =db.Column(db.Numeric(10,3), nullable=False)
    shortw=db.Column(db.Numeric(10,3), nullable=False)
    rate=db.Column(db.Numeric(10,2), nullable=False)
    remarks = db.Column(db.String(2), nullable=False)
    amt=db.Column(db.Numeric(10,2), nullable=False)
    adv=db.Column(db.Numeric(10,2), nullable=False)
    hsdadv=db.Column(db.Numeric(10,2), nullable=False)
    hsdliter=db.Column(db.Numeric(10,2), nullable=False)
    bal=db.Column(db.Numeric(10,2), nullable=False)

    
    def __repr__(self)->str:
        return f"{self.cweight}-{self.rweight}"


@app.route('/',methods=['GET','POST'])
def homepage():
    #THIS IS JUST A BASIC LOGIC
    if request.method=='POST':
        username=request.form['username']
        passw=request.form['pass']
        if username=='jbt' and passw=='cbsajbt': 
            return redirect("/party")
        else:
            return redirect("/")
    return render_template('login.html')


@app.route('/party', methods=['GET','POST'])
def party():
    
    if request.method=='POST':
        global key
    
        if request.form['submit']=='1':
            
            key=1
            return redirect('/test')
        if request.form['submit']=='2':
            
            key=2
            return redirect('/test')
        if request.form['submit']=='3':
            
            key=3
            return redirect('/test')
        if request.form['submit']=='4':
            
            key=4
            return redirect('/test')
        if request.form['submit']=='5':
            
            key=5
            return redirect('/test')
        if request.form['submit']=='6':
            
            key=6
            return redirect('/test')
        if request.form['submit']=='7':
            
            key=7
            return redirect('/test')
        if request.form['submit']=='8':
            
            key=8
            return redirect('/test')
        if request.form['submit']=='9':
            
            key=9
            return redirect('/test')
        
        if request.form['submit']=='10':
            
            key=10
            return redirect('/test')
        
        if request.form['submit']=='999':
            
            key=999
            return redirect('/test')
    return render_template('party.html')


@app.route('/test', methods=['GET','POST'])
def test():
    
    if request.method=='POST':
       
        if request.form['submit']=='submit':
            date_created=request.form['date_created']
            truckno=request.form['truckno']
            cweight =request.form['cweight']
            rweight=request.form['rweight']
            rate=request.form['rate']
            remarks=request.form['remarks']
            amt=Decimal(rate)*Decimal(rweight)
            adv=request.form['adv']
            hsdadv=request.form['hsdadv']
            hsdliter=request.form['hsdliter']
            shortw=Decimal(cweight)-Decimal(rweight)
            bal=Decimal(amt)-(Decimal(adv)+Decimal(hsdadv))
            entries=Entries(truckno=truckno,cweight=cweight,date_created=date_created, rweight=rweight, amt=amt, hsdadv=hsdadv,
            hsdliter=hsdliter, adv=adv,bal=bal,party=key,rate=rate, remarks=remarks,shortw=shortw)
            db.session.add(entries)
            db.session.commit()
            print(cweight, rweight)
        if request.form['submit']=='search':
            
            return redirect('/searchs')
        if request.form['submit']=='excel':
            
            return redirect('/searchs')
        if request.form['submit']=='back':
            key=""
            return redirect('/party')
        
    allentries= Entries.query.order_by(desc(Entries.date_created)).filter_by(party=key).all()

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
        date_created=request.form['date_created']
        truckno=request.form['truckno']
        cweight =request.form['cweight']
        rweight=request.form['rweight']
        rate=request.form['rate']
        remarks=request.form['remarks']
        adv=request.form['adv']
        hsdadv=request.form['hsdadv']
        hsdliter=request.form['hsdliter']
        entries=Entries.query.filter_by(sno=sno).first()
        entries.date_created=date_created
        entries.truckno=truckno
        entries.cweight=cweight
        entries.rweight=rweight
        entries.rate=rate
        entries.remarks=remarks
        entries.adv=adv
        entries.hsdadv=hsdadv
        entries.hsdliter=hsdliter
        entries.shortw=Decimal(entries.cweight)-Decimal(entries.rweight)
        entries.amt=Decimal(entries.rate)*Decimal(entries.rweight)
        entries.bal=Decimal(entries.amt)-(Decimal(entries.adv)+Decimal(entries.hsdadv))
        db.session.add(entries)
        db.session.commit()
        return redirect("/test")
    entries= Entries.query.filter_by(sno=sno).first()
    return render_template('update.html',entries=entries)


@app.route('/allparty',methods=['GET','POST'])
def allparty():
    
    return render_template('allparty.html')

#EXCEL FILE WORK
def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict


@app.route('/excel', methods=['GET', 'POST'])
def exportexcel():
    
    data = Entries.query.all()
    data_list = [to_dict(item) for item in data]
    df = pd.DataFrame(data_list)
    cols=df.columns.tolist()
    cols=cols[::-1]
    df=df[cols]
    rowcount,columncount=df.shape
    #print(rowcount,columncount)
    if rowcount< 3001:
        df_split=df[0:3001]
        filename = "./static/Entries_11.xlsx"  #app.config['JBT']+
        writer = pd.ExcelWriter(filename)
        df_split.to_excel(writer, sheet_name='Entries')
        writer.save()
        
    if rowcount> 3000 and rowcount< 6001:
       
        df_split=df[3000:6001]
        filename = "./static/Entries_22.xlsx"  
        writer = pd.ExcelWriter(filename)
        df_split.to_excel(writer, sheet_name='Entries')
        writer.save()
        
    if rowcount> 6000 and rowcount< 9001:
       
        df_split=df[6000:9001]
        filename = "./static/Entries_33.xlsx"  
        writer = pd.ExcelWriter(filename)
        df_split.to_excel(writer, sheet_name='Entries')
        writer.save()
        
    if rowcount> 9000 and rowcount< 12001:
       
        df_split=df[9000:12001]
        filename = "./static/Entries_44.xlsx"  
        writer = pd.ExcelWriter(filename)
        df_split.to_excel(writer, sheet_name='Entries')
        writer.save()

    return render_template('excel.html',rowcount=rowcount)
                          

if __name__ == '__main__':
    app.run(debug=True)
