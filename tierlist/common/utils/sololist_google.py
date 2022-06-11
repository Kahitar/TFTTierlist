from dataclasses import dataclass
from typing import List
import requests
from bs4 import BeautifulSoup

@dataclass
class TierlistRow:
    tier: int
    subtier: int
    carries: str
    synergies: str
    positioning_link: str

def get_tierlist() -> List[TierlistRow]:
    html = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQXGfKXwmtXV3JXkkvFW9kcvXtWdEpXq-5uohygcek-qM19CvuWTZYf5VwrgXqwMBVLhVomP0yp_jEZ/pubhtml').text
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table")
    tierlist = []
    for idx, table in enumerate(tables):
        rows = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")]
        tierlist_started = False
        last_tier, curr_tier, curr_subtier = 1, 1, 0
        for row in rows:
            if len(row) == 0:
                continue

            if not tierlist_started:
                if row[0] == "RANKING":
                    tierlist_started = True
                continue

            if row[1] == "":
                # end of tierlist assumed when the "carries" column is empty
                break

            try:
                curr_tier = int(row[0].replace("TIER", "").strip())
                curr_subtier = 0 if curr_tier > last_tier else curr_subtier+1
            except ValueError:
                # The comp has no tier
                curr_subtier += 1

            tierlist.append(TierlistRow(
                tier=curr_tier,
                subtier=curr_subtier,
                carries=row[1],
                synergies=row[2],
                positioning_link=row[3],
            ))
    return tierlist


if __name__ == "__main__":
    tierlist = get_tierlist()
    for row in tierlist:
        print(row)