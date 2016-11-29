from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models

from profiles.models import UserProfile


GAME_STATES = [
    "IN_PROGRESS", "FAIL", "WIN",
]


class Game(models.Model):
    session_id = models.CharField(_("Session ID"), max_length=128, blank=False)
    phrase = models.CharField(_("Phrase"), max_length=128, blank=False)
    progress = models.CharField(_("Progress"), max_length=128, blank=False)
    used_characters = models.CharField(_("Used letters"), max_length=128, blank=False)
    score = models.IntegerField(_("Score"), default=0)
    mistakes = models.IntegerField(_("Mistakes"), default=0)
    max_mistakes = models.IntegerField(_("Max mistakes"), default=5)
    player = models.ForeignKey(UserProfile, null=True)
    inverse_death = models.BooleanField(_("Inverse death"), default=False)

    def update_round(self):
        all_rounds = self.round_set.all()
        if len(all_rounds) <= 0:
            return
        else:
            game_round = all_rounds[0]
            for game in game_round.games.all():
                if game.state == GAME_STATES[2]:
                    return
            if self.state == GAME_STATES[2]:
                game_round.winner = self.player
                game_round.save()

    @property
    def state(self):
        condition = self.get_winning_condition()
        if condition == GAME_STATES[2] and self.inverse_death:
            return GAME_STATES[1]
        elif condition == GAME_STATES[1] and self.inverse_death:
            return GAME_STATES[2]

        return condition

    def __unicode__(self):
        return "%s [%s]" % (self.progress, self.session_id)

    def get_winning_condition(self):
        # if phrase is guessed
        if self.phrase == self.progress:
            return GAME_STATES[2]
        # if used more than 5 incorrect chars, fail
        elif self.mistakes >= self.max_mistakes:
            return GAME_STATES[1]

        # game still in progress
        return GAME_STATES[0]


class Tournament(models.Model):
    name = models.CharField(_("Tournament name"), max_length=255)
    players = models.ManyToManyField(UserProfile)
    current_round = models.IntegerField(_("Current round"), default=0)
    mode = models.IntegerField(_("Game mode"), default=0)
    tournament_mode = models.IntegerField(_("Tournament mode"), default=0)
    session_id = models.CharField(_("Session ID"), max_length=128, blank=False)
    in_progress = models.BooleanField(_("Is in progress?"), default=True)


class Round(models.Model):
    round_id = models.IntegerField(_("This round ID"))
    tournament = models.ForeignKey(Tournament)
    games = models.ManyToManyField(Game)
    winner = models.ForeignKey(UserProfile)
