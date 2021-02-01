from flask import render_template, url_for, redirect, request, Blueprint, request
from tierlist.main.forms import SearchForm
from tierlist.users.utils import get_users_tierlists, get_users_posts
from tierlist.models import Comp, Tierlist, Post, User


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/<int:active_tierlist_id>")
@main.route("/home")
@main.route("/home/<int:active_tierlist_id>")
def home(active_tierlist_id=None):
    home_user = User.query.filter_by(username="Sologesang").first()
    if home_user:
        username = home_user.username
    else:
        username = User.query.first().username
    return redirect(url_for('users.profile', username=username))


@main.route("/search", methods=["GET", "POST"])
@main.route("/search/<string:query>", methods=["GET", "POST"])
def search(query=None):

    search_term = request.form.get("search_username")
    if search_term:
        users = User.query.filter(User.username.contains(search_term)).all()
        if len(users) == 1:
            return redirect(url_for('users.profile', username=users[0].username))
        return redirect(url_for('main.search', query=search_term))

    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_term = search_form.query.data
        if search_term:
            users = User.query.filter(User.username.contains(search_term)).all()
            if len(users) == 1:
                return redirect(url_for('users.profile', username=users[0].username))
        else:
            users = User.query.all()
        return render_template('search_result.html', search_form=search_form, users=users)

    if query:
        search_form.query.data = query
        users = User.query.filter(User.username.contains(query)).all()
        if len(users) == 1:
            return redirect(url_for('users.profile', username=users[0].username))
    else:
        users = User.query.all()
    return render_template('search_result.html', search_form=search_form, users=users)


@main.route("/admin", methods=["GET", "POST"])
def admin():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_term = search_form.query.data
        if search_term == "":
            users = User.query.all()
        else:
            users = User.query.filter(User.username.contains(search_term))
        return render_template('admin_console.html', search_form=search_form, users=users)
    all_users = User.query.all()
    return render_template('admin_console.html', search_form=search_form, users=all_users)


@main.route("/about")
@main.route("/impressum")
def impressum():
    return render_template('about.html')
