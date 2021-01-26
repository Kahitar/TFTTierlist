import tierlist
from tierlist import create_app, db
from tierlist.models import User, Tierlist, Comp, Post

app = create_app()


def main():
    # create_db()
    manage()


def create_db():
    with app.app_context():
        db.create_all()

        admin = User(username="Admin", email="Niklasarens1@gmx.de",
                     is_admin=True, password="xxx")
        new_tierlist = Tierlist(author=admin)

        db.session.add(admin)
        db.session.add(new_tierlist)
        db.session.commit()


def manage():
    with app.app_context():
        # user_1 = User.query.first()
        # list_1 = Tierlist.query.first()

        # for user in User.query.all():
        #     user.is_admin = False

        # post = Post.query.all()
        # db.session.commit()
        # user = User.query.all()

        # list_1.name = "Live"
        # print(list_1)
        # db.session.commit()

        print("Is main:", Tierlist.query.first().is_main)
        print(Tierlist.query.filter_by(is_main=True).all())


if __name__ == '__main__':
    main()
