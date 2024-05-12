import functools
from flask import (g, redirect, url_for)
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user = g.get("user")
        if user is None:
            return redirect(url_for('auth.doctor_sign_in'))

        return view(**kwargs)

    return wrapped_view