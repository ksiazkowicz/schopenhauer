# -*- coding: utf-8 -*-
import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models

from profiles.models import UserProfile
from .helpers import get_quote
from .signals import new_tournament_round


GAME_STATES = [
    "IN_PROGRESS", "FAIL", "WIN",
]

MODIFIERS_VERBOSE = {
    "inverse_death": u"Born To Die",
    "only_one_mistake": u"YOLO",
    "cooperation": u"Wszyscy mamy źle w głowach, że żyjemy",
    "no_modifiers": u"Eutanazol",
}


def get_verbose_modifiers(modifiers):
    """
    Parses the list of modifiers and returns a verbose string.
    """
    if modifiers:
        modifier_list = modifiers.split(";")
        if not modifier_list:
            return MODIFIERS_VERBOSE["no_modifiers"]
        return ", ".join([MODIFIERS_VERBOSE.get(x, "")
                          for x in modifier_list
                          if x in MODIFIERS_VERBOSE.keys()])
    return "Eutanazol"


class Game(models.Model):
    session_id = models.CharField(_("Session ID"), max_length=128, blank=False)
    phrase = models.CharField(_("Phrase"), max_length=128, blank=False)
    progress = models.CharField(_("Progress"), max_length=128, blank=False)
    used_characters = models.CharField(
        _("Used letters"), max_length=128, blank=False)
    score = models.IntegerField(_("Score"), default=0)
    mistakes = models.IntegerField(_("Mistakes"), default=0)
    player = models.ForeignKey(UserProfile, null=True)
    modifiers = models.CharField(_("Modifiers"), max_length=256, default="")

    @property
    def is_ranking_game(self):
        return "cooperation" not in self.modifiers

    def verbose_mode(self):
        return get_verbose_modifiers(self.modifiers)

    @property
    def get_mistake_count(self):
        if "only_one_mistake" in self.modifiers:
            if self.mistakes != 0:
                return 5
        return self.mistakes

    @property
    def max_mistakes(self):
        """
        Return max mistake count.
        """
        if "only_one_mistake" in self.modifiers:
            return 1
        return 5

    @property
    def progress_string(self):
        guessed = len(self.progress)-self.progress.count("_")
        return "%s/%s" % (guessed, len(self.progress))

    def update_round(self):
        """
        Checks if any game in round ended and ends it if we won.
        """
        all_rounds = self.round_set.all()
        if len(all_rounds) <= 0:
            return
        else:
            game_round = all_rounds[0]
            for game in game_round.games.all():
                if game.state == GAME_STATES[2] and game != self:
                    return
            if self.state == GAME_STATES[2]:
                game_round.winner = self.player
                game_round.save()

    @property
    def state(self):
        condition = self.get_winning_condition()
        return condition

    def __str__(self):
        return "%s [%s]" % (self.progress, self.session_id)

    def get_winning_condition(self):
        """
        Checks if game is in progress, won or failed.
        :return: returns a string, either "IN_PROGRESS", "WIN" or "FAIL"
        """
        # check how many mistakes were made already
        if self.mistakes >= self.max_mistakes:
            return "FAIL"

        # with modifiers, it's more complicated
        if "inverse_death" in self.modifiers:
            if self.phrase == self.progress:
                # you're not supposed to guess phrases
                return "FAIL"
            # ok, this is complicated, cause we need to check if ALL LETTERS
            # THAT AREN'T IN THAT PHRASE ARE USED let's make a set of all
            # letters, the ones that are in the phrase and substract them
            remaining_letters = set(u"aąbcćdeęfghijklłmnńoprsśtuówyzżź")
            phrase_letters = set(self.phrase)
            # this should give us letters that aren't in the phrase
            remaining_letters.difference_update(phrase_letters)
            # substract used characters
            remaining_letters.difference_update(set(self.used_characters))
            if not remaining_letters:
                # yay we won
                return "WIN"
        else:
            # follow regular rules
            if self.phrase == self.progress:
                return "WIN"

        # game still in progress
        return GAME_STATES[0]

    def get_user_permissions(self, user):
        """
        Check if user has permission to guess letters in this game.
        """
        if self.round_set.all().count():
            # if we have cooperation enabled, every tournament participant can
            # guess
            if "cooperation" in self.modifiers:
                this_round = self.round_set.all().first()
                return user in this_round.tournament.players.all()
        # if player is defined, compare given user to that, otherwise let the
        # shitfest begin
        if self.player:
            return self.player == user
        return True

    def guess(self, user, letter):
        """
        Guesses the letter.
        :param letter: letter to guess
        :param user: user who is guessing
        :return: outcome (fail/win)
        """
        # check if user has permissions to guess letters
        if not self.get_user_permissions(user):
            return False

        # check if game is in progress
        if not self.state == "IN_PROGRESS":
            return False

        player = self.player

        # assume we failed
        outcome = False

        # make sure letter is lowercase
        letter = letter.lower()

        if letter not in "aąbcćdeęfghijklłmnńoprsśtuówyzżź":
            return False

        # check if character is already used
        if letter not in self.used_characters:
            # ok, we can do stuff, count the letter as used first
            self.used_characters += letter

            # check if letter is guessed
            guessed = letter in self.phrase.lower()

            # update game progress data if guessed
            if guessed:
                # create a new variable for new progress string
                new_progress = ""

                # iterate through all letters
                for index, org_letter in enumerate(self.phrase.lower()):
                    if letter == org_letter:
                        new_progress += self.phrase[index]
                        outcome = True
                    else:
                        new_progress += self.progress[index]

                # update progress
                self.progress = new_progress

            # time to get those modifiers to work
            if "inverse_death" in self.modifiers:
                # you shouldn't be guessing letters in this mode, you know
                if guessed:
                    self.mistakes += 1
                else:
                    # get as many points as there are remaining spaces
                    self.score += self.progress.count("_")
                    if self.is_ranking_game:
                        player.score += self.progress.count("_")
                        player.save()

            else:
                # regular rules enforced
                if not guessed:
                    self.mistakes += 1
                else:
                    self.score += self.phrase.count(letter)
                    if self.is_ranking_game:
                        player.score += self.phrase.count(letter)
                        player.save()

        # save changes
        self.save()
        self.update_round()

        # update player if it's a ranking game
        if self.state != "IN_PROGRESS" and self.is_ranking_game:
            if self.state == "WIN":
                player.won_games += 1
            else:
                player.lost_games += 1
            player.save()

        return outcome


def create_game(user, modifiers=None, phrase=None):
    """
    Creates a game for given user, with given parameters (modifiers, phrase)
    Returns game object.
    """
    if not phrase:
        phrase = get_quote()

    game_progress = ""
    for x in phrase:
        if x.isalpha():
            game_progress += "_"
        else:
            game_progress += x

    game = Game.objects.create(session_id=uuid.uuid1().hex, phrase=phrase,
                               progress=game_progress, used_characters="",
                               player=user, modifiers=modifiers)
    return game


class Tournament(models.Model):
    name = models.CharField(_("Tournament name"), max_length=255)
    players = models.ManyToManyField(UserProfile)
    admin = models.ForeignKey(
        UserProfile, related_name="tournament_admin", default=True)
    current_round = models.IntegerField(_("Current round"), default=0)
    session_id = models.CharField(_("Session ID"), max_length=128, blank=False)
    in_progress = models.BooleanField(_("Is in progress?"), default=True)
    modifiers = models.CharField(_("Modifiers"), max_length=256, default="")
    public = models.BooleanField(_("Is public?"), default=False)

    def __str__(self):
        return "[%s] %s" % (
            "Trwający" if self.in_progress else "Zakończony", self.name)

    def verbose_mode(self):
        return get_verbose_modifiers(self.modifiers)

    def get_admin(self):
        """
        Returns tournament admin.
        """
        if self.admin:
            return self.admin
        else:
            return self.players.all()[0]

    def create_new_round(self):
        """
        Creates a new round and games that are a part of it.
        """
        # create a new round object
        new_round = Round.objects.create(round_id=self.current_round+1,
                                         tournament=self)
        self.current_round += 1
        self.save()

        # generate a common phrase
        phrase = get_quote()

        # if cooperation enabled, create just one game
        game = None
        coop_game = None
        if "cooperation" in self.modifiers:
            coop_game = create_game(None, phrase=phrase,
                                    modifiers=self.modifiers)
            new_round.games.add(coop_game)
            game = coop_game

        # iterate through list of players, create games and push out redirects
        for player in self.players.all():
            # create new game if we're not in coop mode
            if not coop_game:
                game = create_game(player, phrase=phrase,
                                   modifiers=self.modifiers)
                new_round.games.add(game)

            # push out info to everyone
            new_tournament_round.send(
                sender=self.__class__, instance=self, game_id=game.session_id,
                player=player)

    def end_tournament(self):
        """
        Ends the tournament and updates the scoreboard.
        """
        self.in_progress = False

        if self.winner:
            winner = self.winner
            winner.won_tournaments += 1
            winner.save()
        for player in self.players.all():
            if player != self.winner:
                player.lost_tournaments += 1
                player.save()
        self.save()

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

    def get_winner(self):
        # really stupid workaround
        if "cooperation" in self.tournament.modifiers:
            if self.games.all().count() > 0:
                if self.games.all()[0].state == "WIN":
                    return "Wszyscy"
            return "Nikt"
        else:
            return self.winner.username if self.winner else ""

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
        return u"Zakończona"


class ChatMessage(models.Model):
    author = models.ForeignKey(UserProfile)
    message = models.CharField(_("Message"), max_length=255)
    context = models.CharField(_("Context"), max_length=255)
    timestamp = models.DateTimeField(_("Time"), auto_now=True)
