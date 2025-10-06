from django.core.cache import cache
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            key = f'rl:{request.user.username}'
            limit = 50
        else:
            ip = request.META.get('HTTP_X_FORWARDED_FOR')
            if ip:
                ip = ip.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')    
        
            key = f'rl:{ip}'
            limit = 100

        count = cache.get(key, 0)
        if count >= limit:
            return HttpResponseForbidden("Too many requests")

        cache.set(key, count + 1, timeout=60)
        return self.get_response(request)