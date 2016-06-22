import django.dispatch


session_replaced = django.dispatch.Signal(providing_args=['request', 'src_domain', 'dest_domain', 'was_empty'])
