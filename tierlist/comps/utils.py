

def get_max_subtier(comps):
    max_subtier = 0
    for comp in comps:
        if comp.sub_tier > max_subtier:
            max_subtier = comp.sub_tier
    return max_subtier


def get_same_tier_comps(comp, all_comps):
    same_tier = [c for c in all_comps if c.tier == comp.tier and c is not comp]
    same_tier.sort(key=lambda c: c.sub_tier)
    return same_tier


def tier_up(comp, all_comps):
    old_tier_comps = get_same_tier_comps(comp, all_comps)
    old_sub_tier = comp.sub_tier
    comp.tier -= 1
    new_tier_comps = get_same_tier_comps(comp, all_comps)

    # Fix sub-tiers of old tier
    for c in old_tier_comps:
        if c.sub_tier > old_sub_tier:
            c.sub_tier -= 1

    if comp.tier <= 0:
        tier_down(comp, all_comps)
    else:
        max_subtier = get_max_subtier(new_tier_comps)
        comp.sub_tier = max_subtier + 1


def tier_down(comp, all_comps):
    old_tier_comps = get_same_tier_comps(comp, all_comps)
    old_sub_tier = comp.sub_tier
    comp.tier += 1
    comp.sub_tier = 1
    new_tier_comps = get_same_tier_comps(comp, all_comps)

    # Fix sub-tiers of old tier
    for c in old_tier_comps:
        if c.sub_tier > old_sub_tier:
            c.sub_tier -= 1

    for c in new_tier_comps:
        c.sub_tier += 1


def sub_tier_up(comp, all_comps):
    tier_comps = get_same_tier_comps(comp, all_comps)  # not including comp

    if comp.sub_tier <= 1:
        tier_up(comp, all_comps)
    else:
        comp.sub_tier -= 1

        # Fix comp's sub-tiers
        for c in tier_comps:
            if c.sub_tier == comp.sub_tier:
                c.sub_tier += 1


def sub_tier_down(comp, all_comps):
    tier_comps = get_same_tier_comps(comp, all_comps)  # not including comp
    max_sub_tier = get_max_subtier(tier_comps)  # not including comp

    if comp.sub_tier > max_sub_tier:
        tier_down(comp, all_comps)
    else:
        comp.sub_tier += 1

        # Fix comp's sub-tiers
        for c in tier_comps:
            if c.sub_tier == comp.sub_tier:
                c.sub_tier -= 1
