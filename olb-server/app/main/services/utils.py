from enum import Enum

PLATINUM_UPPER = 0
PLATINUM_LOWER = 0.10
GOLD_UPPER = 0.10
GOLD_LOWER = 0.30
SILVER_UPPER = 0.30
SILVER_LOWER = 0.60
BRONZE_UPPER = 0.60
BRONZE_LOWER = 1


class RankIcon(Enum):
    PLATINUM = 1
    GOLD = 2
    SILVER = 3
    BRONZE = 4


def get_rank_icon(rank, total_members):
    top_percentile = rank/total_members

    if(top_percentile > BRONZE_UPPER and top_percentile <= BRONZE_LOWER):
        rank_icon = RankIcon.BRONZE
    elif(top_percentile > SILVER_UPPER and top_percentile <= SILVER_LOWER):
        rank_icon = RankIcon.SILVER
    elif(top_percentile > GOLD_UPPER and top_percentile <= GOLD_LOWER):
        rank_icon = RankIcon.GOLD
    elif(top_percentile > PLATINUM_UPPER and top_percentile <= PLATINUM_LOWER):
        rank_icon = RankIcon.PLATINUM
    else:
        rank_icon = RankIcon.BRONZE

    return rank_icon
