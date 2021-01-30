import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from tierlist import mail
from tierlist.models import Tierlist, Comp, Post


def get_users_tierlists(users, only_public=True):
    if only_public:
        tierlists_nested = [Tierlist.query.filter_by(is_public=1, author=user).all() for user in users] # This is not very efficient, but there should only ever be a few admins.
    else:
        tierlists_nested = [Tierlist.query.filter_by(author=user).all() for user in users]
    tierlists = [t_list for l in tierlists_nested for t_list in l]
    all_comps = []
    for t_list in tierlists:
        all_comps.append(Comp.query.filter_by(tierlist=t_list).order_by(
            Comp.tier.asc(), Comp.sub_tier.asc()).all())

    return (tierlists, all_comps)

def get_users_posts(users):
    posts_nested = [Post.query.filter_by(author=user).all() for user in users] # This is not very efficient with a lot of users.
    posts = [t_list for l in posts_nested for t_list in l]

    return posts


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    # Resize picture
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def delete_picture(picture_filename):
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_filename)
    if os.path.isfile(picture_path):
        os.remove(picture_path)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='weight-assist@gmx.de', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no change will be made.
'''
    mail.send(msg)
