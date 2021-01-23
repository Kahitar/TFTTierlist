from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from tierlist import db
from tierlist.models import Comp, Tierlist
from tierlist.comps.forms import CompForm
from tierlist.tierlist.utils import update_tierlist

comps = Blueprint('comps', __name__)


@comps.route('/comp/new', methods=["GET", "POST"])
@login_required
def new_comp():
    form = CompForm()
    if form.validate_on_submit():
        comp = Comp(tier=0,
                    sub_tier=0,
                    carries=form.carries.data,
                    synergies=form.synergies.data,
                    lolchess=form.lolchess.data,
                    chosen=form.chosen.data,
                    tierlist=Tierlist.query.first())
        db.session.add(comp)
        db.session.commit()
        update_tierlist(list_id=Tierlist.query.first().id)
        flash("The comp has been created.", "success")
        return redirect(url_for('main.home'))
    return render_template('create_comp.html', title='New Comp',
                           form=form, legend="New Comp")


@comps.route("/comp/<int:comp_id>/update", methods=["GET", "POST"])
@login_required
def update_comp(comp_id):
    comp = Comp.query.get_or_404(comp_id)
    if not current_user.is_admin:
        abort(403)

    form = CompForm()
    if form.validate_on_submit():
        comp.carries = form.carries.data
        comp.synergies = form.synergies.data
        comp.lolchess = form.lolchess.data
        comp.chosen = form.chosen.data
        db.session.commit()
        update_tierlist(list_id=Tierlist.query.first().id)
        flash("The comp has been updated.", "success")
        return redirect(url_for("main.home"))
    elif request.method == "GET":
        form.carries.data = comp.carries
        form.synergies.data = comp.synergies
        form.lolchess.data = comp.lolchess
        form.chosen.data = comp.chosen
    return render_template('create_comp.html', title='Update Comp',
                           form=form, legend="Update Comp")


@comps.route("/comp/<int:comp_id>/<string:direction>/move")
def move_comp(comp_id, direction):
    comp = Comp.query.get_or_404(comp_id)

    # TODO: Calculate
    MAX_SUBTIER = 3

    if direction == 'tier-up':
        comp.tier -= 1
    if direction == 'tier-down':
        comp.tier += 1
    if direction == 'up':
        comp.sub_tier -= 1
    if direction == 'down':
        comp.sub_tier += 1

    if comp.sub_tier <= 0 and comp.tier > 1:
        comp.tier -= 1
        comp.sub_tier = MAX_SUBTIER + 1
    elif comp.sub_tier >= MAX_SUBTIER + 1:
        comp.tier += 1
        comp.sub_tier = 1
    elif comp.sub_tier <= 0:
        comp.sub_tier = 1
    if comp.tier <= 0:
        comp.tier = 1

    db.session.commit()

    return redirect(url_for('main.home'))


@comps.route("/comp/<int:comp_id>/delete", methods=["POST"])
@login_required
def delete_comp(comp_id):
    comp = Comp.query.get_or_404(comp_id)
    if comp.tierlist.author != current_user:
        abort(403)

    db.session.delete(comp)
    db.session.commit()
    update_tierlist(list_id=Tierlist.query.first().id)
    flash("The comp has been deleted.", "success")
    return redirect(url_for('main.home'))
