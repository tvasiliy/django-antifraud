from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tor, Checker
from .serializers import TorSerializer, CheckerSerializer
from .utils import check_ip_is_proxy
API_RESULT_OK = 'ok'
API_RESULT_ERROR = 'error'


class ListTorView(generics.ListAPIView):
    queryset = Tor.objects.all()
    serializer_class = TorSerializer


class ListHistoryView(generics.ListAPIView):
    queryset = Checker.objects.all()
    serializer_class = CheckerSerializer


@api_view(['GET', 'POST'])
def check_device(request, *args, **kwargs):
    if 'ip' in request.query_params:
        ip = request.query_params.get('ip')
        result = Tor.objects.filter(tor_ip=ip).first()
        is_tor = result is not None
        is_proxy = check_ip_is_proxy(ip)

        response = {
            'ip': ip,
            'result': API_RESULT_OK,
        }
        # save result
        try:
            result_log = Checker()
            result_log.ip = ip
            result_log.is_tor = is_tor
            result_log.is_proxy = is_proxy
            result_log.full_clean()
            result_log.save()
            # set result
            response['is_tor'] = is_tor
            response['is_proxy'] = is_proxy
        except ValidationError as e:
            # set error
            response['result'] = API_RESULT_ERROR
            response['message'] = e.messages

        return Response(response)
    else:
        return Response({
            'result': API_RESULT_OK,
            'message': 'Missing required parameters'},
            status=status.HTTP_400_BAD_REQUEST
        )
