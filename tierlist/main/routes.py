from flask import render_template, request, Blueprint
from tierlist.models import Comp, Tierlist, Post


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    tierlist = Tierlist.query.filter_by(is_main=1).first()
    if tierlist is None:
        # If there's no main tierlist, just get the first result
        tierlist = Tierlist.query.first()
    comps = Comp.query.filter_by(tierlist=tierlist).order_by(
        Comp.tier.asc(), Comp.sub_tier.asc()).all()

    posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template('home.html', comps=comps, tierlist=tierlist, posts=posts, title="Sologesang")


@main.route("/about")
@main.route("/impressum")
def impressum():
    return render_template('about.html')
