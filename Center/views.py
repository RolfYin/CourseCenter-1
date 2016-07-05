import io

from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse, HttpRequest

# Create your views here.
from Center.models import Student


def download(request):
    with open('H:/BaiduYunDownload/31 - Green Bird.flac', "r+b") as fd:
        data = fd.read()
    response = HttpResponse(data, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="31 - Green Bird.flac"'
    return response


def upload(request):
    assert isinstance(request, HttpRequest)
    # with open("test.jpg", "w+b") as fd:
    #     fd.write(request.body)-0

    print(st)
    assert isinstance(request.FILES["Filedata"].file, io.BytesIO)
    print(request.FILES["Filedata"])
    print(request.FILES["Filedata"].file.read())
    return HttpResponse("OK")


def login(request):
    assert isinstance(request, HttpRequest)
    st = Student.objects.filter(sid=int(request.POST["idNumber"]), spassword=request.POST["Password"])
    print(request.body)
    s = SessionStore()
    s.set_expiry(60)
    s.save()
    print(s.session_key)
    s.clear_expired()
    return HttpResponse("hello")


def logout(request):
    assert isinstance(request, HttpRequest)
    return HttpResponse("OK")


def view_course(request):
    assert isinstance(request, HttpRequest)
    return HttpResponse("OK")
