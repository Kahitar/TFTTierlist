from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from tierlist import db
from tierlist.models import Tierlist, Comp
from tierlist.tierlist.forms import TierlistPropertiesForm

tierlists = Blueprint('tierlists', __name__)


@tierlists.route('/tierlist/create', methods=["GET", "POST"])
@login_required
def new_tierlist():
    form = TierlistPropertiesForm()

    if form.validate_on_submit():
        name = form.name.data
        is_public = form.is_public.data
        new_tierlist = Tierlist(author=current_user,
                                name=name, is_public=is_public)
        db.session.add(new_tierlist)
        db.session.commit()
        flash("New Tierlist has been created.", "success")
        return redirect(url_for('tierlists.manage', active_tierlist_id=new_tierlist.id))

    return render_template('tierlist_properties.html', form=form, legend="Create New Tierlist")


@tierlists.route('/tierlist/<int:tierlist_id>/properties', methods=["GET", "POST"])
@login_required
def tierlist_properties(tierlist_id):
    tierlist = Tierlist.query.get_or_404(tierlist_id)
    form = TierlistPropertiesForm()
    if form.validate_on_submit():
        tierlist.name = form.name.data
        tierlist.is_public = form.is_public.data
        db.session.commit()
        flash("The tierlist has been updated.", "success")
        return redirect(url_for('tierlists.manage', active_tierlist_id=tierlist.id))
    elif request.method == 'GET':
        form.name.data = tierlist.name
        form.is_public.data = tierlist.is_public
    return render_template('tierlist_properties.html', form=form, tierlist=tierlist, legend="Tierlist Properties")


@tierlists.route('/tierlist/manage')
@tierlists.route('/tierlist/manage/<int:active_tierlist_id>')
@login_required
def manage(active_tierlist_id=None):
    tierlists = Tierlist.query.filter_by(author=current_user).all()
    all_comps = []
    for t_list in tierlists:
        all_comps.append(Comp.query.filter_by(tierlist=t_list).order_by(
            Comp.tier.asc(), Comp.sub_tier.asc()).all())
    if active_tierlist_id:
        active_tierlist = Tierlist.query.get_or_404(active_tierlist_id)
    else:
        active_tierlist = None
    return render_template("tierlists.html", tierlists=tierlists, all_comps=all_comps, active_tierlist=active_tierlist)


@tierlists.route("/tierlist/<int:tierlist_id>/delete", methods=["POST"])
@login_required
def delete_tierlist(tierlist_id):
    tierlist = Tierlist.query.get_or_404(tierlist_id)
    if tierlist.author != current_user:
        abort(403)

    # Delete all comps of this tierlist
    for comp in tierlist.comps:
        db.session.delete(comp)
    # Delete the tierlist itself
    db.session.delete(tierlist)
    db.session.commit()
    flash("Your tierlist has been deleted.", "success")
    return redirect(url_for('tierlists.manage'))
