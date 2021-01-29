from flask import render_template, request, Blueprint
from tierlist.models import Comp, Tierlist, Post, User


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/<int:active_tierlist_id>")
@main.route("/home")
@main.route("/home/<int:active_tierlist_id>")
def home(active_tierlist_id=None):
    admins = User.query.filter_by(is_admin=True).all()
    tierlists_nested = [Tierlist.query.filter_by(is_public=1, author=admin).all() for admin in admins] # This is not very efficient, but there should only ever be a few admins.
    tierlists = [t_list for l in tierlists_nested for t_list in l]
    all_comps = []
    for t_list in tierlists:
        all_comps.append(Comp.query.filter_by(tierlist=t_list).order_by(
            Comp.tier.asc(), Comp.sub_tier.asc()).all())
    if active_tierlist_id:
        active_tierlist = Tierlist.query.get_or_404(active_tierlist_id)
    else:
        active_tierlist = None

    posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template('home.html', tierlists=tierlists, all_comps=all_comps, active_tierlist=active_tierlist, posts=posts, title="Sologesang")


@main.route("/about")
@main.route("/impressum")
def impressum():
    return render_template('about.html')
