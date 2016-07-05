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
    data = json.loads(request.body.decode())
    result = HttpResponse(json.dumps({}))
    p = []
    if int(data["type"]) == 3:
        p = Student.objects.filter(sid=int(data["ID"]), spassword=data["Password"])
    elif int(data["type"]) == 2:
        p = Teacher.objects.filter(tid=data["ID"], tpassword=data["Password"])
    if len(p):
        s = SessionStore()
        s.set_expiry(160)
        s["ID"] = data["ID"]
        s["type"] = data["type"]
        s.save()
        s.clear_expired()
        result = HttpResponse(json.dumps({"name": p[0]["sName"], "key": s.session_key}))
    return result


def logout(request):
    assert isinstance(request, HttpRequest)
    return HttpResponse("OK")


def view_course(request):
    assert isinstance(request, HttpRequest)
    data = json.loads(request.body.decode())
    key = data["key"]
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
