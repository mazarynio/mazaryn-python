from django.http import HttpResponse


def ping(request):
    return HttpResponse("All good", status=200)