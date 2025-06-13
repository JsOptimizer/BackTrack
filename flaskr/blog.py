from flask import (Blueprint,flash,url_for,g,render_template,redirect,request)

from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp=Blueprint("blog",__name__)

