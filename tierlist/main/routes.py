from flask import render_template, request, Blueprint
from tierlist.models import Comp, Tierlist


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    comps = Comp.query.order_by(Comp.tier.asc(), Comp.sub_tier.asc()).all()
    tierlist = Tierlist.query.first()
    return render_template('tierlist.html', comps=comps, tierlist=tierlist, title="Sologesang")


@main.route("/about")
@main.route("/impressum")
def impressum():
    return render_template('about.html')
