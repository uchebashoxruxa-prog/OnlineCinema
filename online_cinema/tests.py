from django.test import TestCase

# Create your tests here.
def get_client_ip(request):
    x = request.META.get('HTTP_X_FORWARDED_FOR')
    if x:
        ip = x.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
