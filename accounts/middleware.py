from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import logout


class AutoLogout(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_authenticated:
            # Can't log out if not logged in
            return self.get_response(request)

        try:
            if datetime.now() - request.session["last_touch"] > timedelta(
                0, settings.AUTO_LOGOUT_DELAY * 60, 0
            ):
                logout(request)
                del request.session["last_touch"]
                return self.get_response(request)
            else:
                request.session["last_touch"] = datetime.now()
                return self.get_response(request)
        except KeyError:  # KeyError thrown if last touch doesn't exist, so set it.
            request.session["last_touch"] = datetime.now()

        return self.get_response(request)
