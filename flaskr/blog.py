from flask import(
    Blueprint,flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required

from flaskr.db import get_db

bp=Blueprint('blog', __name__)
@bp.route('/index')
def index():
    db = get_db()  # This gives you the connection
    cur = db.cursor()  # Create a cursor from the connection
    cur.execute(
        '''SELECT p.id, p.title, p.body, p.created, p.author_id, u.username 
           FROM post AS p 
           JOIN user1 AS u ON p.author_id = u.id 
           ORDER BY p.created DESC'''
    )
    posts = cur.fetchall()  # Fetch all the results
    cur.close()  # Close the cursor after use
    return render_template('blog/index.html', posts=posts)


@bp.route('/create',methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            cur = db.cursor()  # Create a cursor
            cur.execute(
                'INSERT INTO post (title, body, author_id) VALUES (%s, %s, %s)',
                (title, body, g.user['id'])
            )
            db.commit()
            cur.close()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    db = get_db()
    cur = db.cursor()  # Create a cursor
    cur.execute(
        '''SELECT p.id, p.title, p.body, p.created, p.author_id, u.username 
           FROM post AS p 
           JOIN user1 AS u ON p.author_id = u.id 
           WHERE p.id = %s''',
        (id,)
    )
    post = cur.fetchone()  # Fetch a single result
    cur.close()  # Close the cursor

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post

@bp.route('/<int:id>/update',methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.cursor()  # Create a cursor
            cur.execute(
                '''UPDATE post SET title = %s, body = %s WHERE id = %s''',
                (title, body, id)
            )
            db.commit()  # Commit the changes
            cur.close()  # Close the cursor
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete',methods=('GET', 'POST'))
@login_required
def delete(id):
    post = get_post(id)
    db = get_db()
    cur = db.cursor()  # Create a cursor
    cur.execute('''DELETE FROM post WHERE id = %s''', (id,))
    db.commit()  # Commit the changes
    cur.close()  # Close the cursor
    return redirect(url_for('blog.index'))