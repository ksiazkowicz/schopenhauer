import json
from channels import Group
from django.dispatch import receiver
from game.models import Tournament
from . import new_tournament_round


@receiver(new_tournament_round, sender=Tournament)
def push_redirect(sender, instance, **kwargs):
    """
    Redirect everyone on signal.
    """
    game = kwargs.pop("game_id")
    player = kwargs.pop("player")
    Group("tournament-%s" % instance.session_id).send({
        "text": json.dumps({
            "game": game,
            "player": player.username,
            "redirect": True
        })
    })
