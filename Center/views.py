import io
import json

from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse, HttpRequest

# Create your views here.
from Center.models import *


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
    assert isinstance(request.FILES["Filedata"].file, io.BytesIO)
    print(request.FILES["Filedata"])
    print(request.FILES["Filedata"].file.read())
    return HttpResponse("OK")


def login(request):
    assert isinstance(request, HttpRequest)
    st = Student.objects.filter(sid=int(request.POST["ID"]), spassword=request.POST["Password"])
    if len(st):
        s = SessionStore()
        s.set_expiry(160)
        s["ID"] = request.POST["ID"]
        s["type"] = request.POST["type"]
        s.save()
        s.clear_expired()
        result = HttpResponse(json.dumps({"name": "sName", "key": s.session_key}))
    else:
        result = json.dumps({})
    return result


def logout(request):
    assert isinstance(request, HttpRequest)
    return HttpResponse("OK")


def view_course(request):
    assert isinstance(request, HttpRequest)
    key = request.POST["key"]
    s = SessionStore(session_key=key)
    s.set_expiry(160)
    s.save()
    courses = []
    if int(s["type"]) == 3:
        courses_id = Studentcourse.objects.filter(sid=s["ID"])
        for course_id in courses_id:
            courses.append(Course.objects.filter(cid=course_id))
    elif int(s["type"]) == 2:
        courses = Course.objects.filter(teacherid=s["ID"])
    return HttpResponse(json.dumps(courses))
