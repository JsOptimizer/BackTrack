from flask import (g,Blueprint,flash,redirect,render_template,session,url_for,request)

from werkzeug.security import (check_password_hash,generate_password_hash)
from flaskr.db import (get_db)

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

