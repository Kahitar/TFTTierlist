import tierlist
from tierlist import create_app, db
from tierlist.models import User, Tierlist, Comp

app = create_app()

with app.app_context():
    user_1 = User.query.first()
    list_1 = Tierlist.query.first()


new_comp = Comp(
    Tierlist=list_1,
    tier=1, sub_tier=4, carries="Morgana", synergies="Enlightened",
    lolchess="https://lolchess.gg/builder/set4.5?deck=1a189980582611ebb2e1d9dd6894f398",
    chosen="Enlightened")

with app.app_context():
    db.session.add(new_comp)
    db.session.commit()
