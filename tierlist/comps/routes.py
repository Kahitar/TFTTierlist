from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from tierlist import db
from tierlist.models import Comp, Tierlist
from tierlist.comps import utils
from tierlist.comps.forms import CompForm
from tierlist.tierlist.utils import update_tierlist, fix_subtier_gaps

comps = Blueprint('comps', __name__)


@comps.route('/comp/<int:tierlist_id>/new', methods=["GET", "POST"])
@login_required
def new_comp(tierlist_id):
    form = CompForm()
    if form.validate_on_submit():
        comp = Comp(tier=6,
                    sub_tier=0,
                    carries=form.carries.data,
                    synergies=form.synergies.data,
                    lolchess=form.lolchess.data,
                    chosen=form.chosen.data,
                    tierlist=Tierlist.query.get_or_404(tierlist_id))
        db.session.add(comp)
        db.session.commit()
        update_tierlist(Tierlist.query.get_or_404(tierlist_id))
        flash("The comp has been created.", "success")
        return redirect(url_for('tierlists.manage', active_tierlist_id=tierlist_id))
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
        update_tierlist(comp.tierlist)
        flash("The comp has been updated.", "success")
        return redirect(url_for('tierlists.manage', active_tierlist_id=comp.tierlist.id))
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
    all_comps = Comp.query.filter_by(tierlist=comp.tierlist).all()

    if direction == 'tier-up':
        utils.tier_up(comp, all_comps)
    if direction == 'tier-down':
        utils.tier_down(comp, all_comps)
    if direction == 'up':
        utils.sub_tier_up(comp, all_comps)
    if direction == 'down':
        utils.sub_tier_down(comp, all_comps)

    update_tierlist(comp.tierlist)
    db.session.commit()
    return redirect(url_for('tierlists.manage', active_tierlist_id=comp.tierlist.id))


@comps.route("/comp/<int:comp_id>/delete", methods=["POST"])
@login_required
def delete_comp(comp_id):
    comp = Comp.query.get_or_404(comp_id)
    if comp.tierlist.author != current_user:
        abort(403)

    db.session.delete(comp)
    db.session.commit()
    update_tierlist(comp.tierlist)
    flash("The comp has been deleted.", "success")
    return redirect(url_for('tierlists.manage', active_tierlist_id=comp.tierlist.id))
