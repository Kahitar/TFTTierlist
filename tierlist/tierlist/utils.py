from datetime import datetime
from tierlist import db
from tierlist.models import Tierlist, Comp


def update_tierlist(list_id):
    tierlist = Tierlist.query.filter_by(id=list_id).first()
    comps = Comp.query.filter_by(tierlist=tierlist).all()
    print("Comps:", comps)

    for comp in comps:
        if comp.tier == 0:
            pass

    tierlist.last_updated = datetime.now()
    print(tierlist.last_updated)

    db.session.commit()
