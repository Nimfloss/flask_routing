from functools import wraps
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,g
import pymysql
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SubmitField
from passlib.hash import sha256_crypt
import email_validator

app = Flask(__name__)
app.secret_key = "justforfun"

import pymysql

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session["logged_in"] == True and session["username"] != "":
                return f(*args, **kwargs)
            else:
                flash("You must be logged in to view this page.","warning")
                return redirect(url_for("login"))
        except KeyError:
            flash("You need to log in again due to some server errors.","warning")
            return redirect(url_for("login"))
    return decorated_function

# Login required decorator for user-only routes.
def isloggedin():
    try:
        if session["logged_in"] == True and session["username"] != "":
            return True
        else:
            return False
    except KeyError:
        return False

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="new_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# For debugging mysql con. (I got too many mysql errors. That's why I wrote it.)
def mysql_connectiontest():
    try:
        connect = get_db_connection()
        cursor = connect.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchall()
        return "Connection to MySQL is successful. {}".format(data)
    except Exception as e:
        return "There is an error while connecting to MySQL:\n{}".format(e)

# Registeration
class Registeration(Form):
    name = StringField(validators = [validators.Length(min = 1,max = 50),validators.DataRequired()])
    username = StringField(validators = [validators.Length(min = 4 ,max = 50),validators.DataRequired()])
    email = StringField(validators = [validators.Email(message = "Please type valid email..."),validators.DataRequired()])
    password = PasswordField(validators = [validators.Length(min=8,max=50),validators.DataRequired(),validators.EqualTo(fieldname= "confirm",message="Your password do not match.")])
    confirm = PasswordField(validators=[validators.DataRequired()])
    submit = SubmitField("Register")

class Login(Form):
    username = StringField(validators = [validators.DataRequired()])
    password = PasswordField(validators=[validators.DataRequired()])
    submit = SubmitField("Login")

class Passch(Form):
    oldpass = PasswordField(validators =[validators.DataRequired()])
    newpass = PasswordField(validators =[validators.DataRequired()])
    newpasscon = PasswordField(validators =[validators.DataRequired()])
    submit = SubmitField("Change Password")

class Addarticle(Form):
    subject = StringField(validators = [validators.DataRequired(),validators.Length(3,200)])
    content = TextAreaField(validators = [validators.DataRequired()])
    submit = SubmitField("Publish Article")

#Index way
@app.route("/")
def index():
    return render_template("index.html")

#Articles way
@app.route("/articles")
def articles():
    return render_template("articles.html")

#Register way
@app.route("/register",methods = ["GET","POST"])
def register():
    form = Registeration(request.form)
    if (request.method == "POST"):
        if form.validate():
            name = form.name.data
            username = form.username.data
            password = sha256_crypt.encrypt(form.password.data)
            email = form.email.data
            connect = get_db_connection()
            cursor = connect.cursor()
            user_check = "Select * from users where username = %s"
            cursor.execute(user_check,(username,))
            users_list = cursor.fetchone()
            if users_list is None:
                insert = "Insert into users(name,email,username) VALUES(%s,%s,%s,%s)"
                cursor.execute(insert,(name,email,username,password))
                connect.commit()
                cursor.close()
                connect.close()
                print("Register Completed.")
                flash("Successfully registered.","success")
                return redirect(url_for("login"))
            else:
                flash("This username is already taken.","warning")
                return redirect(url_for("register"))
        else:
            flash("There was a problem! Your registration was not completed!","danger")
            flash("Check your information.","warning")
            return redirect(url_for("register"))
    if request.method == "GET":
        return render_template("register.html",form = form)

#Login way
@app.route("/login",methods = ["GET","POST"])
def login():
    form = Login(request.form)
    if request.method == "GET":
        return render_template("login.html",form=form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        connect = get_db_connection()
        cursor = connect.cursor()
        check = "Select * from users where username = %s"
        cursor.execute(check,(username,))
        info=cursor.fetchone()

        if info is None:
            flash("Username and password didn't matched.","warning")
            cursor.close()
            connect.close()
            return redirect(url_for("login"))
        else:
            password_hashed = info["password"]
            if sha256_crypt.verify(password,password_hashed):
                flash("Login successful.","success")
                session["logged_in"] = True
                session["username"] = username
                cursor.close()
                connect.close()
                return redirect(url_for("index"))
            else:
                flash("Password and username did not matched.","warning")

                cursor.close()
                connect.close()
                return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():
    session["logged_in"] = False
    session["username"] = ""
    flash("Successfully logged out.","success")
    return render_template("index.html")

@app.route("/passch",methods = ["GET","POST"])
@login_required
def passch():
    form = Passch(request.form)
    if request.method == "GET":
        try:
            if session["username"] != "":
                return render_template("passch.html",form = form)
        except KeyError:
            flash("Your account cannot be accessed for some reason(?). Please log in again.","danger")
            return redirect(url_for("logout"))
    elif request.method == "POST":
        oldpassw = form.oldpass.data
        newpassw = form.newpass.data
        newpassconw = form.newpasscon.data
        check = "Select * from users where username = %s"
        connect = get_db_connection()
        cursor = connect.cursor()
        active_username = session["username"]
        cursor.execute(check,(active_username,))
        info = cursor.fetchone()
        fatched_password = info["password"]
        if sha256_crypt.verify(oldpassw,fatched_password):
            if newpassw == newpassconw:
                n_hash_pass = sha256_crypt.encrypt(newpassw)
                update_f = "UPDATE users SET password = %s WHERE username = %s"
                cursor.execute(update_f,(n_hash_pass,active_username))
                connect.commit()
                cursor.close()
                connect.close()
                flash("Your password was successfully changed.","success")
                return redirect(url_for("index"))
            else:
                flash("Your new passwords didn't matched","warning")
                cursor.close()
                connect.close()
                return redirect(url_for("passch"))

        else:
            flash("Your old password does not match","danger")
            cursor.close()
            connect.close()
            return redirect(url_for("passch"))


@app.route("/myaccount")
@login_required
def myaccount():
    return render_template("myaccount.html")


# Serve dynamic article pages based on article ID.
@app.route("/articles/<string:id>")
def article_string(id):
    return render_template("articles/{}.html".format(id))

@app.route("/addarticle",methods = ["GET","POST"])
@login_required
def addarticle():
    form = Addarticle(request.form)
    if request.method == "GET":
        return render_template("addarticle.html",form = form)
    elif request.method == "POST":
        if form.validate():
            subject = form.subject.data
            content = form.content.data
            active_user = session["username"]

            connect = get_db_connection()
            cursor = connect.cursor()

            insert = "Insert into articles(title,author,content) VALUES(%s,%s,%s)"

            cursor.execute(insert,(subject,active_user,content))
            connect.commit()
            cursor.close()
            connect.close()

            flash("Your article published successfully.","success")
            return redirect(url_for("articles"))
        else:
            flash("Something went wrong...","warning")
            return redirect(url_for("addarticle"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("nonfound.html"),404

print(mysql_connectiontest())

#Debug starter
if __name__ == "__main__":
    app.run(debug=True)
