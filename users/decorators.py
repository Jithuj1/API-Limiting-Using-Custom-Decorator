from django.core.cache import cache
from django.http import HttpResponse

def rate_limit_calls(rate_limit):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            cache_key = f'rate_limit:{request.user.id}' 

            count = cache.get(cache_key, 0)

            if count >= rate_limit:
                return HttpResponse('Rate limit exceeded. Please try again later.', status=429)

            cache.set(cache_key, count + 1, timeout=None)

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator