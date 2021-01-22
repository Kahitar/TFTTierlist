from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from tierlist import db
from tierlist.models import Comp, Tierlist
from tierlist.comps.forms import CompForm

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
        flash("The comp has been created.", "success")
        return redirect(url_for('main.home'))
    return render_template('create_comp.html', title='New Comp',
                           form=form, legend="New Comp")


@comps.route("/comp/<int:post_id>")
def comp(post_id):
    comp = Post.query.get_or_404(post_id)
    return render_template("comp.html", title=comp.title, comp=comp)


@comps.route("/comp/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    comp = Post.query.get_or_404(post_id)
    if comp.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        comp.title = form.title.data
        comp.content = form.content.data
        db.session.commit()
        flash("Your comp has been updated!", "success")
        return redirect(url_for("comps.comp", post_id=comp.id))
    elif request.method == "GET":
        form.title.data = comp.title
        form.content.data = comp.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend="Update Post")


@comps.route("/comp/<int:comp_id>/delete", methods=["POST"])
@login_required
def delete_comp(comp_id):
    comp = Comp.query.get_or_404(comp_id)
    if comp.tierlist.author != current_user:
        abort(403)

    db.session.delete(comp)
    db.session.commit()
    flash("Your comp has been deleted!", "success")
    return redirect(url_for('main.home'))
