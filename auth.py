import functools
from psycopg2 import extras
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request,
    session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db_operator.base_manager import PostgresBaseManager
from db_operator.delete_data import delete_user_location


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    print(f"Current user: {user_id}")
    if user_id is None:
        g.user = None
    else:
        postgres_manager = PostgresBaseManager()
        cur = postgres_manager.conn.cursor(cursor_factory=extras.DictCursor)
        try:
            cur.execute('SELECT * FROM usr WHERE id = (%s);', (user_id,))
        except Exception as e:
            print("Read failed.")
            print(e)
        finally:
            g.user = cur.fetchone()
            cur.close()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = str(request.form['username'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        postgres_manager = PostgresBaseManager()
        cur = postgres_manager.conn.cursor(cursor_factory=extras.DictCursor)

        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        try:
            cur.execute('SELECT id FROM Usr WHERE email = (%s);', (email,))
            if cur.fetchone() is not None:
                error = 'Email {} is already registered.'.format(email)

            if error is None:
                cur.execute(
                    'INSERT INTO Usr (usrName, email, password) VALUES (%s, %s, %s);',
                    (username, email, generate_password_hash(password))
                )
                postgres_manager.conn.commit()
                cur.close()
                current_app.logger.info("User %s has been created.", username)
                return redirect(url_for('auth.login'))

        except Exception as e:
            print("Read failed.")
            print(e)

        current_app.logger.error(error)
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = str(request.form['email'])
        password = str(request.form['password'])
        postgres_manager = PostgresBaseManager()
        cur = postgres_manager.conn.cursor(cursor_factory=extras.DictCursor)
        error = None
        try:
            cur.execute('SELECT * FROM Usr WHERE email = (%s);', (email,))

        except Exception as e:
            print("Read failed.")
            print(e)
        finally:
            user = cur.fetchone()
            cur.close()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            current_app.logger.info(
                "User %s (%s) has logged in.", user['usrname'], user['id']
            )
            return redirect(url_for('index'))

        current_app.logger.error(error)
        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    if g.user is not None:
        current_app.logger.info(
            "User %s (%s) has signed out.", g.user['usrname'], g.user['email']
        )
        delete_user_location(g.user["id"])
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
