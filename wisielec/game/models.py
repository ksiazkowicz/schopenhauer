from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models


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

    @property
    def state(self):
        return self.get_winning_condition

    def __unicode__(self):
        return "%s [%s]" % (self.progress, self.session_id)

    @property
    def get_winning_condition(self):
        # if phrase is guessed
        if self.phrase == self.progress:
            return GAME_STATES[2]
        # if used more than 5 incorrect chars, fail
        elif self.mistakes >= 5:
            return GAME_STATES[1]

        # game still in progress
        return GAME_STATES[0]
