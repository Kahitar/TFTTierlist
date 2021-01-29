from flask import render_template, url_for, redirect, request, Blueprint
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
        user_id = home_user.id
    else:
        user_id = User.query.first().id
    return redirect(url_for('users.profile', user_id=user_id))


@main.route("/search/<string:query>", methods=["GET", "POST"])
@main.route("/search", methods=["GET", "POST"])
def search(query=None):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_term = search_form.query.data
        if search_term == "":
            users = User.query.all()
        else:
            users = User.query.filter(User.username.contains(search_term))
        return render_template('search.html', search_form=search_form, users=users)
    all_users = User.query.all()
    return render_template('search.html', search_form=search_form, users=all_users)


@main.route("/about")
@main.route("/impressum")
def impressum():
    return render_template('about.html')
