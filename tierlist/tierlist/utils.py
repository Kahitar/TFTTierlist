from datetime import datetime
from tierlist import db
from tierlist.models import Tierlist, Comp


def update_tierlist(tierlist):
    fix_subtier_gaps(tierlist)
    tierlist.last_updated = datetime.now()
    db.session.commit()


def fix_subtier_gaps(tierlist):
    all_comps = Comp.query.filter_by(tierlist=tierlist).all()
    all_comps.sort(key=lambda c: float(f"{c.tier}.{c.sub_tier:05}"))

    next_subtier = 1
    current_tier = 0
    for comp in all_comps:
        if comp.tier > current_tier:
            current_tier = comp.tier
            next_subtier = 1

        if comp.sub_tier != next_subtier:
            comp.sub_tier = next_subtier
        next_subtier += 1

    db.session.commit()
