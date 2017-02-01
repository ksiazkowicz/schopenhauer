from django import template

register = template.Library()

@register.simple_tag
def won_rounds(player, tournament):
    """
    Returns count of won rounds by player for given tournament
    """
    if "cooperation" in tournament.modifiers:
        return len([x for x in tournament.round_set.all() if x.get_winner() != "Nikt"])
    else:
        won_rounds = tournament.round_set.filter(winner=player)
        return won_rounds.count()
