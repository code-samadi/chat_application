import os
from flask import Flask
from flaskr.db import get_db, close_db


def create_app(test_config=None):
    app=Flask(__name__,instance_relative_config=True)

    # configuration of the app
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE_NAME=os.getenv('DATABASE_NAME'),
        DATABASE_USER=os.getenv('DATABASE_USER'),
        DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD'),
        DATABASE_HOST=os.getenv('DATABASE_HOST'),
        DATABASE_PORT=os.getenv('DATABASE_PORT'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try :
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.route('/hello')
    def hello():
        return 'Hello World'

    # Running the sql files
    from . import db

    db.init_app(app)

    app.teardown_appcontext(close_db)

    # Blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    return app
    