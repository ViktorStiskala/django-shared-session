# django-shared-session

django-shared-session is a tool that enables cross site session sharing, which can be useful when running the same Django
application on different domains (for example due to different language mutations). This library can be used for sharing login information as well as session data for both authenticated and anonymous users. If all you need is to share login information, please  consider using some of single sign-on (SSO) solutions which could be better for this specific use case. 

This tool is only useful when you are running your application on different domains, not just subdomains. Subdomains can be handled with cookies path set to `.domain.tld` (start's with dot).

This project is inspired by [django-xsession](https://github.com/badzong/django-xsession), but uses a different approach to session sharing which sets the cookie on server-side and thus does not require reloading the page.

## How it works

1. User visits one of the configured sites
2. Session key is encrypted and included in the HTML file. This file contains `<script>` tags linking to all configured sites with encrypted session key (as part of the file name).
3. Browser requests the script files
4. On destination domain the session key is decrypted from payload and saved to cookies

Example HTML snippet:
```html
<script src="http://www.example.org/shared-session/9x7JV1xWFAk8nWhORGCkO5O4zUSjVCR-2abQh7AnFRckiwk8adn6PVlCsdqX4SaTY2dde7S3YuM0ZchKsCuZZiYSZwVLtOA5IoUJRHDl74s4uBYQERQQQMh6T48WD883cFvAaI0XVKB1d5YVtZ7st7GIfxUv2kw6JqftQnFb7uhAOtbTrbdsVWdJEQYdBbweoQPRm9BiRodpk8oo6gpKKC434jPLnJX4-B31KhessmVrgC6_7AOjyZUypC52JXAEjZQm.js" async></script>
<script src="http://www.another-domain.org/shared-session/v_artye4YSMnbbqrrBzUqmIIBFArsMRIkH9vIBNqiEM3uMJQF2RMJtLifIaehbMxRG-ChyMB3gDyLTGmbtCOhs1ODcFAy0PdekJHlSoLR3xezvDCld0YBbfDoOQFVqPeTavHx2uF7X-6A5bWRtV19hg5kI4uFDKWHATCxm2EdXZPrkN23nX_2-PUfCufAQR3vJeJQRjSzj-FfX-qK9xxAeL1-rvUwJvb2bCvoqL0gCTMNBMSeXLMkjjlpXmmlAfGeU3C.js" async></script>
```
Encrypted payload (containing session key, timestamp, source and destination hostname) in base64 is part of the filename itself. Destination server checks the timestamp to prevent replay attacks.

## Installation

```sh
pip install django-shared-session
```

This tool accesses request inside template, so please make sure you have `RequestContext` enabled in your template's engine context processors.

## Usage
Add `shared_session` to `INSTALLED_APPS` and set shared session domains in Django settings file.
Then add `shared_session.urls` to your urlconf. 

settings.py:
```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    'shared_session'
]

SHARED_SESSION_SITES = ['www.example.com', 'www.example.org']
```

urls.py:
```py
import shared_session

urlpatterns = [
    url(r'^shared-session/', shared_session.urls),  # feel free to change the base url
]
```

In order to share sessions with configured sites you also need to use `{% shared_session_loader %}` in your base template.

layout.html:
```html
{% load shared_session %}

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        {% shared_session_loader %}
    </head>
    <body>
        
    </body>
</html>
```

If you want to share sessions also in Django admin interface, you can overwrite `admin/base_site.html` and include the loader.

## Advanced options

`SHARED_SESSION_ALWAYS_REPLACE` – Always replace session cookie, even if the session is not empty. (default: False)
`SHARED_SESSION_TIMEOUT` – Expiration timeout. Session needs to be delivered to destination site before this time. (default: 30)

### Signals

Signal `session_replaced` is triggered when target's site session cookie was changed or created.
You can connect your own handlers to run additional functions.

```py
from shared_session import signals
import logging

def log_session_replace(sender, **kwargs):
    logging.info('%s session replaced' % kwargs.get('dst_domain'))

signals.session_replaced.connect(log_session_replace)
```

## License

This software is licensed under MPL 2.0.

- http://mozilla.org/MPL/2.0/
- http://www.mozilla.org/MPL/2.0/FAQ.html#use
