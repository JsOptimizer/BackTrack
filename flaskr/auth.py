from flask import (g,Blueprint,flash,redirect,render_template,session,url_for,request)

from werkzeug.security import (check_password_hash,generate_password_hash)
from flaskr.db import (get_db)
import functools
bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route("/register",methods=('GET','POST'))
def register():
    if request.method=="POST":
        username=request.form['username']
        password=request.form["password"]
        db=get_db()
        error=None

        if not username:
            error="Username is required"
            pass
        elif not password:
            error='Password is required'
            pass
        if error is None:
            try:
                db.execute("INSERT INTO user (username,password) VaLUES (?,?)",(username,generate_password_hash(password)))
                db.commit()
                pass
            except db.IntegrityError:
                error=f"User {username} is already registered."
                pass
            else:
                return redirect(url_for('auth.login'))
            pass
        flash(error)
    return render_template('auth/register.html')

@bp.route('register/login',methods=["GET","POST"])
def login():
    if request.method =='POST':
        username=request.form['username']
        password=request.form['password']
        db=get_db()
        error=None
        user=db.execute("SELECT * FROM user WHERE username =?",(username,)).fetchall()
        if user is None or not check_password_hash(user["password"],password=password):
            error='Incorrect password or username'
            pass
        if error is None:
            session.clear()
            session['user_id']=user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('/auth.login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
        pass
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view