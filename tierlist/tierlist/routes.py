from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required


tierlists = Blueprint('comps', __name__)


@tierlists.route('/tierlist/create', methods=["GET", "POST"])
@login_required
def new_comp():
    new_list = Tierlist(author=current_user)
    db.session.add(new_list)
    db.session.commit()
