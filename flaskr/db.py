import click
import psycopg2
from psycopg2  import extras
from flask import current_app,g

def get_db():
    if 'db' not in g:
        g.db=psycopg2.connect(
            dbname=current_app.config['DATABASE_NAME'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            host=current_app.config['DATABASE_HOST'],
            port=current_app.config['DATABASE_PORT'],
            cursor_factory=psycopg2.extras.DictCursor #added so that whenever a query is asked using a cursor it is returned as dictionary or something like that. To resolve a problem with the login functionality.
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    try:
        with current_app.open_resource('schema.sql', mode='r') as f:
            sql_command=f.read()

        with db.cursor() as cursor:
            for command in sql_command.split(';'):
                command=command.strip()
                if command:
                    cursor.execute(command)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error executing schema: {e}")
        raise

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)