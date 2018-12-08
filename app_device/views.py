from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_device.models import Tor, Checker
from app_device.serializers import TorSerializer, CheckerSerializer


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
        result = Tor.objects.filter(tor_ip=ip)
        if result is None:
            return Response({'ip': ip, 'status': 'notfound'})
        else:
            return Response({'ip': ip, 'status': 'found'})
    else:
        return Response({
            'message': 'Missing required parameters'},
            status=status.HTTP_400_BAD_REQUEST
        )
