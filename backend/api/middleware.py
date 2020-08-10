import sys

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response

from .models import WebUser
from .utils import get_second_domain


class DomainFilter(MiddlewareMixin):
    def process_request(self, request):
        second_domain = get_second_domain(request.headers.get('host'))
        valid_users = {user[0] for user in WebUser.objects.values_list('u_website_domain')}
        if second_domain not in valid_users and request.path.find('/api/admin/') == -1:
            # return HttpResponseForbidden('<h1>bye bye ^-^</h1>')
            return HttpResponseRedirect(f"{request.scheme}://xpick.cn")


class UserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
