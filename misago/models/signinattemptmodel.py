from datetime import timedelta
from django.db import models
from django.utils import timezone
from misago.conf import settings

class SignInAttemptsManager(models.Manager):
    """
    IP's that have exhausted their quota of sign-in attempts are automatically banned for set amount of time.

    That IP ban cuts bad IP address from signing into board by either making another sign-in attempts or
    registering "fresh" account.
    """
    def register_attempt(self, ip):
        attempt = SignInAttempt(ip=ip, date=timezone.now())
        attempt.save(force_insert=True)

    def is_jammed(self, ip):
        # Limit is off, dont jam IPs?
        if settings.attempts_limit == 0:
            return False
        # Check jam
        if settings.jams_lifetime > 0:
            attempts = SignInAttempt.objects.filter(
                                                    date__gt=timezone.now() - timedelta(minutes=settings.jams_lifetime),
                                                    ip=ip
                                                    )
        else:
            attempts = SignInAttempt.objects.filter(ip=ip)
        return attempts.count() > settings.attempts_limit


class SignInAttempt(models.Model):
    ip = models.GenericIPAddressField()
    date = models.DateTimeField()

    objects = SignInAttemptsManager()

    class Meta:
        app_label = 'misago'