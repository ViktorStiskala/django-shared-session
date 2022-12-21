import django.dispatch


# providing args: request, src_domain, dest_domain, was_empty
session_replaced = django.dispatch.Signal()
