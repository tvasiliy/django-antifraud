from app_device.models import Tor, Checker
from rest_framework import serializers


class TorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tor
        fields = ('id', 'tor_ip', 'tms_created')


class CheckerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Checker
        fields = ('id', 'ip', 'is_tor', 'is_proxy', 'tms_created')
