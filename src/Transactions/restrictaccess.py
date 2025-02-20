from functools import wraps
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy

def RestrictAccessToFrom(view):
    def decorator(func):
        @wraps(func)
        def wrapper_function(self, request, *args, **kwargs):
            if request.META.get("HTTP_REFERER") == request.build_absolute_uri(reverse_lazy(view)):
                return func(self, request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapper_function
    return decorator