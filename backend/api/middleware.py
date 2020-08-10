from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from .models import WebUser
from .utils import get_second_domain


class DomainFilter(MiddlewareMixin):
    def process_request(self, request):
        second_domain = get_second_domain(request.headers.get('host'))
        valid_users = {user[0] for user in WebUser.objects.values_list('u_website_domain')}
        if second_domain not in valid_users and request.path.find('/api/admin/') == -1:
            return HttpResponseForbidden('<h1>bye bye ^-^</h1>')