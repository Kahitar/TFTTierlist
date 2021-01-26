from flask import render_template, request, Blueprint
from tierlist.models import Comp, Tierlist, Post


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    comps = Comp.query.order_by(Comp.tier.asc(), Comp.sub_tier.asc()).all()
    tierlist = Tierlist.query.first()

    posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template('home.html', comps=comps, tierlist=tierlist, posts=posts, title="Sologesang")


@main.route("/about")
@main.route("/impressum")
def impressum():
    return render_template('about.html')
