from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo2.db"
db=SQLAlchemy(app)
app.app_context().push()
class todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(200),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self)->str:
        return f"{self.title}-{self.desc}"
    
        
@app.route('/', methods=["GET","POST"])
def Todo():
    
    
    if request.method=="POST":
        tl=request.form["title"]
        ds=request.form["desc"]
        td=todo(title=tl,desc=ds)
        db.session.add(td)
        db.session.commit()
    alltodo=todo.query.all()
    return  render_template("index.html",alltodo=alltodo)
@app.route("/delete/<int:sno>")
def delete(sno):
    td = todo.query.filter_by(sno=sno).first()
    db.session.delete(td)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:sno>",methods=["POST",'GET'])
def update(sno):
    td1=todo.query.filter_by(sno=sno).first()
    if request.method=="POST":
        tl=request.form["title"]
        ds=request.form["desc"]
        td=todo(title=tl,desc=ds)
        db.session.add(td)
        db.session.delete(td1)
        db.session.commit()
       
        
        return redirect("/")
   
    return render_template("update.html",todo=td1)
 


@app.route("/show")
def all_todo():
    alltodo=todo.query.all()
    print(alltodo)
    return "all todo"



if __name__=='__main__':
    app.run(debug=False)
    
    
