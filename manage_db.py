import tierlist
from tierlist import create_app, db
from tierlist.models import User, Tierlist, Comp

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

        # db.session.commit()
        user = User.query.all()
        print(user)

        tierlist = Tierlist.query.all()


if __name__ == '__main__':
    main()
