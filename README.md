# django-shared-session

django-shared-session is a tool that enables session sharing across multiple domains.
It can be used even for situations where Single sign-on (SSO) is not suitable, e.g.: sharing session data of anonymous users.

This project is inspired by [django-xsession](https://github.com/badzong/django-xsession), but uses a different approach to session sharing
which sets the cookie on server-side and thus does not require reloading the page.

## Installation

```sh
pip install django-shared-session
```

This tool uses request inside template, so please make sure you have enabled `RequestContext` in your template engine context processors.

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

## License

This software is licensed under MPL 2.0.

- http://mozilla.org/MPL/2.0/
- http://www.mozilla.org/MPL/2.0/FAQ.html#use
