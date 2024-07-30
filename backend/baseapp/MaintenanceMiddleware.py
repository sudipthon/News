import ipaddress

from django.conf import \
    settings
from django.http import \
    HttpResponseServerError
from django.shortcuts import \
    render


class MaintenanceMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.MAINTENANCE_MODE:
            allowed_ips = getattr(settings, 'MAINTENANCE_MODE_ALLOWED_IPS', [])
            client_ip = request.META.get('REMOTE_ADDR', None)
            if client_ip and not any(
                ipaddress.ip_address(client_ip) in ipaddress.ip_network(ip) for ip in allowed_ips
            ) and not request.path_info.startswith(settings.STATIC_URL):
                return HttpResponseServerError(render(request, '503.html'))

        response = self.get_response(request)
        return response
