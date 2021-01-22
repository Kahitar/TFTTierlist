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
        print(tierlist)

    # new_comp = Comp(
    #     Tierlist=list_1,
    #     tier=1, sub_tier=4, carries="Morgana", synergies="Enlightened",
    #     lolchess="https://lolchess.gg/builder/set4.5?deck=1a189980582611ebb2e1d9dd6894f398",
    #     chosen="Enlightened")

    # with app.app_context():
    #     db.session.add(new_comp)
    #     db.session.commit()


if __name__ == '__main__':
    main()
