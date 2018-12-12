from django.db import models
from django.core.validators import validate_ipv46_address


class Tor(models.Model):
    tor_ip = models.CharField(
        max_length=40,
        unique=True,
        validators=[validate_ipv46_address],
    )
    is_activated = models.BooleanField(default=True, db_index=True)
    tms_created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.tor_ip

    @staticmethod
    def deactivate_all_ips():
        Tor.objects.filter(is_activated=True).update(is_activated=False)

    @staticmethod
    def remove_old_rows():
        Tor.objects.filter(is_activated=False).delete()


class Checker(models.Model):
    ip = models.CharField(
        max_length=40,
        validators=[validate_ipv46_address],
    )
    is_tor = models.BooleanField(default=None, null=True)
    is_proxy = models.BooleanField(default=None, null=True)
    tms_created = models.DateTimeField(auto_now_add=True, blank=True)
