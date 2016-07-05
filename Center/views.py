import io

from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse, HttpRequest


# Create your views here.
def download(request):
    with open('H:/BaiduYunDownload/31 - Green Bird.flac', "r+b") as fd:
        data = fd.read()
    response = HttpResponse(data, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="31 - Green Bird.flac"'
    return response


def upload(request):
    assert isinstance(request, HttpRequest)
    # with open("test.jpg", "w+b") as fd:
    #     fd.write(request.body)
    assert isinstance(request.FILES["Filedata"].file, io.BytesIO)
    print(request.FILES["Filedata"].file.read())
    return HttpResponse("OK")


def login(request):
    assert isinstance(request, HttpRequest)
    print(request.body)
    s = SessionStore()
    s.set_expiry(60)
    s.save()
    print(s.session_key)
    s.clear_expired()
    return HttpResponse("hello")
