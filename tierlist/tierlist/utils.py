from tierlist import db
from tierlist.models import Tierlist


def update_tierlist(list_id):
    tierlist = Tierlist.query.filter_by(id=list_id).first()
    comps = tierlist.comps

    for comp in comps:
        if comp.tier == 0:
            pass

    db.session.commit()
