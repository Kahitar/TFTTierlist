from flask import render_template, request, Blueprint
from tierlist.models import Comp


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    comps = Comp.query.order_by(Comp.tier.asc(), Comp.sub_tier.asc()).all()
    return render_template('tierlist.html', comps=comps)
