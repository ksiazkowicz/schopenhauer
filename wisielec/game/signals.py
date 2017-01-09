import django.dispatch

new_tournament_round = django.dispatch.Signal(providing_args=["player", "game_id"])
