import requests
from celery import shared_task
from http import HTTPStatus
from .models import Tor


@shared_task
def sync_torlist():
    response = requests.get('https://dan.me.uk/torlist/')
    if response.status_code == HTTPStatus.OK:
        data = response.text.split()
        if len(data) > 0:
            Tor.deactivate_all_ips()
            for ip in data:
                record_tor, created = Tor.objects.get_or_create(tor_ip=ip)
                if not created:
                    record_tor.is_activated = True
                    record_tor.save()
            Tor.remove_old_rows()
    else:
        print('HttpStatus!=Ok' + response.status_code)
