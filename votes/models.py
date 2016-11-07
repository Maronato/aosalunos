
# -*- coding: UTF-8 -*-
from datetime import timedelta
from django.db import models
from django.utils import timezone

# a ideia é ter várias pools diferentes, cada uma com vários votos,
# de forma que possamos alternar
# entre as pools e mostrar votos apenas delas
# cada usuário terá um voto em cada pool
# fazer as pools e os votos o mais genéricos possível


class Poll(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    length = models.PositiveIntegerField(default=0)
    multiple_choice = models.BooleanField(default=False)

    @property
    def end_date(self):
        # if permanent pool
        if self.length == 0:
            return timezone.now() + timedelta(days=1)
        # else
        return self.start_date + timedelta(days=self.length)

    @property
    def over(self):
        if not self.length:
            return False
        return timezone.now() > self.end_date

    def add_option(self, text):
        o = Option(
            poll=self,
            text=text,
        )
        o.save()

    def add_vote(self, profile, option):

        if option not in self.option_set.all():
            return False

        profile_votes = self.vote_set.filter(profile=profile)

        if len(profile_votes) == 0:
            vote = Vote(
                poll=self,
                profile=profile,
                option=option
            )
            vote.save()
            return True

        if self.multiple_choice:
            if option not in [opt.option for opt in profile_votes]:
                vote = Vote(
                    poll=self,
                    profile=profile,
                    option=option
                )
                vote.save()
            return True
        return False


class Vote(models.Model):
    poll = models.ForeignKey(
        'Poll',
        related_name="vote_set",
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        'app.Profile',
        related_name="profile",
        on_delete=models.CASCADE
    )
    option = models.ForeignKey(
        'Option',
        on_delete=models.CASCADE
    )


class Option(models.Model):
    poll = models.ForeignKey('Poll', related_name="option_set")
    text = models.CharField(max_length=300)
