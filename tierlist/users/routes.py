from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from tierlist import db, bcrypt
from tierlist.models import User, Post, Tierlist
from tierlist.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                  RequestResetForm, ResetPasswordForm)
from tierlist.users.utils import (save_picture, delete_picture, send_reset_email,
                                  get_users_tierlists, get_users_posts)


users = Blueprint('users', __name__)


@users.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    # 'SET'
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))

    # 'GET'
    return render_template('register.html', title='Register', form=form)


@users.route('/delete_user/<int:user_id>', methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_admin and current_user != user:
        print("USER:        ", user)
        print("CURRENT USER:", current_user)
        tierlists, all_comps = get_users_tierlists([user], False)
        posts = get_users_posts([user])
        for comps in all_comps:
            for comp in comps:
                db.session.delete(comp)
        for t_list in tierlists:
            db.session.delete(t_list)
        for post in posts:
            db.session.delete(post)
        db.session.delete(user)
        db.session.commit()
        flash(f"Deleted user: {user}", "success")
    elif current_user == user:
        flash("You cannot delete your own account.", "danger")
    else:
        flash("You don't have the permission to do that...", "danger")
    return redirect(url_for('main.search'))


@users.route('/make_admin/<int:user_id>')
@login_required
def make_admin(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_admin:
        user.is_admin = True
        db.session.commit()
        flash(f"Made user admin: {user}", "success")
        return redirect(url_for('main.search'))
    else:
        flash("You don't have the permission to do that...", "danger")
        return redirect(url_for('main.search'))


@users.route('/revoke_admin/<int:user_id>')
@login_required
def revoke_admin(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_admin and current_user != user:
        user.is_admin = False
        db.session.commit()
        flash(f"Revoked admin for user: {user}", "success")
    elif current_user == user:
        flash(f"Cannot revoke admin rights for your own account.", "danger")
    else:
        flash("You don't have the permission to do that...", "danger")
    return redirect(url_for('main.search'))


@users.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data.lower()).first()
        if user:
            try:
                password_match = bcrypt.check_password_hash(
                    user.password, form.password.data)
            except ValueError:
                password_match = False
            if password_match:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))

        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/admin_login/<int:user_id>')
@login_required
def admin_login(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_admin:
        admin = user.is_admin
        login_user(user, remember=False)
        return redirect(url_for('main.admin')) if admin else redirect(url_for('main.home'))


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # Delete old picture
            if current_user.image_file:
                delete_picture(current_user.image_file)
            # Save new picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data.lower()
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('users.account'))  # Post-Get-Redirect-Pattern
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/p/<string:username>")
@users.route("/p/<string:username>/<int:active_tierlist_id>")
def profile(username, active_tierlist_id=None):
    user = User.query.filter_by(username=username).one()
    tierlists, comps = get_users_tierlists([user])
    image_file = url_for(
        'static', filename='profile_pics/' + user.image_file)

    if active_tierlist_id:
        active_tierlist = Tierlist.query.get_or_404(active_tierlist_id)
    else:
        active_tierlist = None

    posts = get_users_posts([user])

    return render_template(
        'user_profile.html',
        title=user.username,
        user=user,
        image_file=image_file,
        tierlists=tierlists,
        all_comps=comps,
        active_tierlist=active_tierlist,
        posts=posts)


@users.route('/reset_password', methods=["GET", "POST"])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/admin_reset_password/<int:user_id>')
def admin_password_reset(user_id):
    user = User.query.get_or_404(user_id)
    token = user.get_reset_token()
    flash(f"Reset Link for user {user}:", 'success')
    flash(f"{url_for('users.reset_password', token=token, _external=True)}", 'success')
    return redirect(url_for('main.search'))


@users.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)

    if user is None:
        flash("That is an invalid or expired token", 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title="Teset Password", form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query\
                .filter_by(author=user)\
                .order_by(Post.date_posted.desc())\
                .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
