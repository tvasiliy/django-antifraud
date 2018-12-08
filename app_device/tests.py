from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Tor, Checker
from .serializers import TorSerializer, CheckerSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_torip(ip=""):
        if ip != "":
            Tor.objects.create(tor_ip=ip)

    @staticmethod
    def create_history(ip="", is_tor=False, is_proxy=False):
        if ip != "":
            Checker.objects.create(ip=ip, is_tor=is_tor, is_proxy=is_proxy)

    def setUp(self):
        # add test data
        self.create_torip("103.234.220.197")
        self.create_torip("2001:49f0:d002:0002:0000:0000:0000:0054")
        self.create_torip("0.0.0.0")
        self.create_torip("127.0.0.1")

        self.create_history("0.0.0.0", True, False)
        self.create_history("127.0.0.1", True, True)
        self.create_history("0.0.0.0", False, False)
        self.create_history("127.0.0.1", False, True)


class GetAllDataTest(BaseViewTest):

    def test_get_all_torlist(self):
        """
        This test ensures that all tor ips added in the setUp method
        exist when we make a GET request to the torlist/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("torlist-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Tor.objects.all()
        serialized = TorSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_history(self):
        """
        This test ensures that all history added in the setUp method
        exist when we make a GET request to the antifraud_history/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("history", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Checker.objects.all()
        serialized = CheckerSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_check_device_invalid(self):
        response = self.client.get(
            reverse("check_device", kwargs={"version": "v1"})
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_check_device_missing_param(self):
        response = self.client.get(
            reverse("check_device", kwargs={"version": "v1"})
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_check_device_valid_and_found(self):
        response = self.client.get(
            reverse("check_device", kwargs={"version": "v1"}),
            {"ip": "2001:49f0:d002:0002:0000:0000:0000:0054"}
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_check_device_valid_and_not_found(self):
        response = self.client.get(
            reverse("check_device", kwargs={"version": "v1"}),
            {"ip": "0.0.0.1"}
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
