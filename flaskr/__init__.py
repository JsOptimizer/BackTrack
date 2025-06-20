import os
from dotenv import load_dotenv
from . import db


load_dotenv()

from flask import Flask

def create_app(test_config=None):
    #Create and config the app
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRETE_KEY="dev",
        DATABASE=os.path.join(app.instance_path,'flask.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        pass
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.route("/")
    def hello():
        return "Hello world"
  
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/",endpoint="index")
    return app
