from flask import Flask,render_template,url_for,request,redirect #Importing necessary flask and modules
from flask_mail import Mail, Message
#from redmail import gmail
from flask_sqlalchemy import SQLAlchemy #Importing the flask-databases
from datetime import datetime 

app=Flask("__main__")#Intansiating flask app
mail = Mail(app)##Intansiating mail
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db=SQLAlchemy(app) 

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#Initialazing the class models
class BlogPost(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(20),nullable=False,default="N/A")
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return "My Post" + str(self.id) 

#Dummy datamodels
mydatas=[
    {"title":"Blog Post1",
    "content":"This is first Blog Post Bruh!",
    "author":"gokul krishnan",
    "date_posted":"Today"
    },
    {"title":"Blog Post2",
    "content":"This is second Blog Post Bruh!",
    "date_posted":"11/11/2022"
    }
    ]
#Home routing 
@app.route("/",methods=["POST","GET"])
def index():
    return render_template("index.html")
    #return ("The number is" + " " + str(num))

#Posts routing 
@app.route("/posts",methods=["POST","GET"])
def posts():
    if request.method == "POST":
        post_title=request.form["title"]
        post_content=request.form["content"]
        post_author=request.form["author"]
        new_post=BlogPost(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
    else:
        mydatas=BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template("posts.html",all_datas=mydatas)

#Delete page routing 
@app.route("/posts/delete/<int:id>")
def delete(id):
    post=BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")

#Update page routing 
@app.route("/posts/update/<int:id>",methods=["GET","POST"])
def update(id):
    post=BlogPost.query.get_or_404(id)
    if request.method == "POST":
        post.title=request.form["title"]
        post.content=request.form["content"]
        post.author=request.form["author"]
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("update.html",i=post)

#About Page routing 
@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html")
"""
mydatas=[
    {"title":"Blog Post1",
    "content":"This is first Blog Post Bruh!",
    "author":"gokul krishnan",
    "date_posted":"Today"
    },
    {"title":"Blog Post2",
    "content":"This is second Blog Post Bruh!",
    "date_posted":"11/11/2022"
    }
    ]
"""
#New_Post Page routing
@app.route("/posts/new_post",methods=["GET","POST"])
def new_post():
    post=BlogPost()
    if request.method == "POST":
        post.title=request.form["title"]
        post.content=request.form["content"]
        post.author=request.form["author"]
        new_post=BlogPost(title=post.title,content=post.content,author=post.author)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("new_post.html",i=post)

#MailNotifications Page routing
@app.route("/mailnotifications", methods=["GET","POST"])
def notify():
   msg = Message(
                'Hi',
                sender ='scarywolf98@gmail.com',
                recipients = ['gokulkrish981997@gmail.com']
               )
   msg.body = 'Hey thanks for subscrbing!'
   mail.send(msg)
   return render_template("mailnotifications.html",msg=msg)
    
#Running our flask    
if __name__ == ("__main__"):
    app.run(debug=True)