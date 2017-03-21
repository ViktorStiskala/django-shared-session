import json
import time

import nacl.secret
from dateutil.parser import parse
from django.conf import settings
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from django.utils import timezone
from django.utils.http import cookie_date, urlsafe_base64_decode
from django.views import View
from nacl.exceptions import CryptoError

from . import signals


class SharedSessionView(View):
    def __init__(self, **kwargs):
        self.encryption_key = settings.SECRET_KEY.encode('ascii')[:nacl.secret.SecretBox.KEY_SIZE]
        super().__init__(**kwargs)

    def decrypt_payload(self, message):
        box = nacl.secret.SecretBox(self.encryption_key)

        data = box.decrypt(message).decode('ascii')
        return json.loads(data)

    def get(self, request, *args, **kwargs):
        response = HttpResponse('', content_type='text/javascript')
        try:
            message = self.decrypt_payload(urlsafe_base64_decode(kwargs.get('message')))

            is_session_empty = request.session.is_empty()

            # replace session cookie only when session is empty or when always replace is set
            if is_session_empty or getattr(settings, 'SHARED_SESSION_ALWAYS_REPLACE', False):
                http_host = request.META['HTTP_HOST']

                if (timezone.now() - parse(message['ts'])).total_seconds() < getattr(settings, 'SHARED_SESSION_TIMEOUT', 30):
                    if request.session.get_expire_at_browser_close():
                        max_age = None
                        expires = None
                    else:
                        max_age = request.session.get_expiry_age()
                        expires_time = time.time() + max_age
                        expires = cookie_date(expires_time)

                    response.set_cookie(
                        settings.SESSION_COOKIE_NAME,
                        message['key'], max_age=max_age,
                        expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        path=settings.SESSION_COOKIE_PATH,
                        secure=settings.SESSION_COOKIE_SECURE or None,
                        httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                    )

                    # ensure CSRF cookie is set
                    get_token(request)

                    # emit signal
                    signals.session_replaced.send(sender=self.__class__, request=request, was_empty=is_session_empty, src_domain=message['src'], dst_domain=http_host)
        except (CryptoError, ValueError):
            pass

        return response


shared_session_view = SharedSessionView.as_view()
