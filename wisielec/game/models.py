# -*- coding: utf-8 -*-
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

    @property
    def progress_string(self):
        return "%s/%s" % (len(self.progress)-self.progress.count("_"), len(self.progress))

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
    admin = models.ForeignKey(UserProfile, related_name="tournament_admin", default=True)
    current_round = models.IntegerField(_("Current round"), default=0)
    mode = models.IntegerField(_("Game mode"), default=0)
    tournament_mode = models.IntegerField(_("Tournament mode"), default=0)
    session_id = models.CharField(_("Session ID"), max_length=128, blank=False)
    in_progress = models.BooleanField(_("Is in progress?"), default=True)

    def get_admin(self):
        """
        Returns tournament admin.
        """
        if self.admin:
            return self.admin
        else:
            return self.players.all()[0]

    @property
    def winner(self):
        """
        Returns a player who won more rounds than anyone else.
        """
        # initialize values
        all_winners = self.round_set.all().values("winner")
        current_player = None
        current_wins = 0

        # iterate through all the players
        for player in self.players.all():
            # count wins
            win_count = len(all_winners.filter(winner=player))
            # check if he won more rounds
            if win_count > current_wins:
                # update data
                current_wins = win_count
                current_player = player

        # return the best one
        return current_player


class Round(models.Model):
    round_id = models.IntegerField(_("This round ID"))
    tournament = models.ForeignKey(Tournament)
    games = models.ManyToManyField(Game)
    winner = models.ForeignKey(UserProfile, null=True, blank=True)

    @property
    def status(self):
        """
        Returns a status of current round.
        - "ROUND_IN_PROGRESS" - games in this round haven't ended yet
        - "ROUND_WON" - round ended and we have a winner
        - "ROUND_FAILED" - round ended but nobody won
        """
        # check if there is a winner first
        if self.winner:
            return "ROUND_WON"
        # iterate through all games
        for game in self.games.all():
            # if any of games is in progress, round haven't ended yet
            if game.state == "IN_PROGRESS":
                return "ROUND_IN_PROGRESS"

        # no games are in progress and there is no winner
        # we fucked up
        return "ROUND_FAILED"

    @property
    def status_verbose(self):
        if self.status == "ROUND_IN_PROGRESS":
            return u"W trakcie"
        else:
            return u"Zakończona"


class ChatMessage(models.Model):
    author = models.ForeignKey(UserProfile)
    message = models.CharField(_("Message"), max_length=255)
    context = models.CharField(_("Context"), max_length=255)
