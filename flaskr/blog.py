from flask import(
    Blueprint,flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required

from flaskr.db import get_db

bp=Blueprint('blog', __name__)
@bp.route('/index')
def index():
    db = get_db()
    posts = db.execute(
        '''SELECT p.id, p.title, p.body, p.created, p.author_id, u.username 
           FROM post AS p 
           JOIN user1 AS u ON p.author_id = u.id 
           ORDER BY p.created DESC'''
    ).fetchall()
    return render_template('blog/index.html',posts=posts)

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
            db=get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id) VALUES (%s, %s, %s)',
                (title,body,g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    db = get_db()
    post = db.execute(
        '''SELECT p.id, p.title, p.body, p.created, p.author_id, u.username 
        FROM post AS p 
        JOIN user1 AS u ON p.author_id = u.id 
        where p.id = %s''',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post

@bp.route('/<int:id>/update',methods=('GET', 'POST'))
@login_required
def update(id):
    post= get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body=request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute(
                '''UPDATE post SET title = %s, body = %s where id = %s''', (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete',methods=('GET', 'POST'))
@login_required
def delete(id):
    get_post(id)
    db=get_db()
    db.execute('''DELETE FROM post WHERE id=%s''',(id,))
    db.commit()
    return redirect(url_for('blog.index'))