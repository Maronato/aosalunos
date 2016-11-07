from django.db import models
from misago.models import User
from party.models import Members


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    ra = models.PositiveIntegerField()
    is_mod = models.BooleanField(default=False)

    # method to get all of the profile's votes in a specific poll
    # def curr_poll_votes(self, poll):

    def make_member(self):
        self.is_mod = True
        self.save()
        m = Members(profile=self)
        m.save()
        return True

    @staticmethod
    def user_from_ra(number):
        try:
            return Profile.objects.get(ra=number).user
        except:
            return None
