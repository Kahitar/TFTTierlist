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
        return redirect(url_for('tierlists.manage'))

    return render_template('tierlist_properties.html', form=form)


@tierlists.route('/tierlist/<int:tierlist_id>/properties', methods=["GET", "POST"])
@login_required
def tierlist_properties(tierlist_id):
    tierlist = Tierlist.query.filter_by(id=tierlist_id).first()
    form = TierlistPropertiesForm()
    if form.validate_on_submit():
        tierlist.name = form.name.data
        tierlist.is_public = form.is_public.data
        db.session.commit()
        flash("The tierlist has been updated.", "success")
        return redirect(url_for('tierlists.manage'))
    elif request.method == 'GET':
        form.name.data = tierlist.name
        form.is_public.data = tierlist.is_public
    return render_template('tierlist_properties.html', form=form)


@tierlists.route('/tierlist/manage')
@login_required
def manage():
    tierlists = Tierlist.query.filter_by(author=current_user).all()
    all_comps = []
    for t_list in tierlists:
        all_comps.append(Comp.query.filter_by(tierlist=t_list).order_by(
            Comp.tier.asc(), Comp.sub_tier.asc()).all())
    return render_template("tierlists.html", tierlists=tierlists, all_comps=all_comps)
