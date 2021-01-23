from datetime import datetime
from tierlist import db
from tierlist.models import Tierlist, Comp


def update_tierlist(list_id):
    tierlist = Tierlist.query.filter_by(id=list_id).first()
    comps = Comp.query.filter_by(tierlist=tierlist)
    print("Comps:", comps)

    for comp in comps:
        if comp.tier == 0:
            pass

    print(type(tierlist.last_updated))
    print(type(datetime.utcnow()))
    tierlist.last_updated = datetime.now()

    db.session.commit()
