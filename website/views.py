from flask import Blueprint, render_template,redirect, url_for
from flask_login import login_required, current_user

views = Blueprint("views", __name__)
@views.route("/")
#@login_required
def home():
    return redirect(url_for('auth.login'))
