from datetime import datetime
from tierlist import db
from tierlist.models import Tierlist, Comp


def tierlist_properties(tierlist):
    fix_subtier_gaps()
    tierlist.last_updated = datetime.now()
    db.session.commit()


def fix_subtier_gaps():
    all_comps = Comp.query.filter_by(tierlist=Tierlist.query.first()).all()
    all_comps.sort(key=lambda c: float(f"{c.tier}.{c.sub_tier}"))

    print("ALL:")
    for comp in all_comps:
        print(comp)

    next_subtier = 1
    current_tier = 0
    for comp in all_comps:
        if comp.tier > current_tier:
            current_tier = comp.tier
            next_subtier = 1

        if comp.sub_tier != next_subtier:
            print(comp.carries)
            print("Correct:", next_subtier)
            print("Actual :", comp.sub_tier)
            comp.sub_tier = next_subtier
            print("New:", comp.sub_tier)
        next_subtier += 1

    db.session.commit()
