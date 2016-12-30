from django import template

register = template.Library()

@register.simple_tag
def won_rounds(player, tournament):
    """
    Returns count of won rounds by player for given tournament
    """
    won_rounds = tournament.round_set.filter(winner=player)
    return len(won_rounds)
