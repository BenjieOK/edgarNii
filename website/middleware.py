from django.shortcuts import redirect
from django.urls import reverse

# Always allowed so local development (manage.py runserver) never locks itself out.
LOCALHOST_IPS = {"127.0.0.1", "::1"}


def get_client_ip(request):
    """Best-effort real client IP, accounting for a reverse proxy in front of the app."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


class AdminIPWhitelistMiddleware:
    """Blocks /admin/ for any IP not in AllowedIP, sending visitors to the access-request page instead."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            from .models import AllowedIP

            ip = get_client_ip(request)
            if ip not in LOCALHOST_IPS and not AllowedIP.objects.filter(ip_address=ip, is_active=True).exists():
                return redirect(f"{reverse('request_access')}?ip={ip}")
        return self.get_response(request)
