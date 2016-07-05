import io
import json

import datetime
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
    if int(data["type"]) == 3:
        p = Student.objects.filter(sid=int(data["ID"]), spassword=data["Password"])
        print(p)
        name = p[0].sname
    elif int(data["type"]) == 2:
        p = Teacher.objects.filter(tid=data["ID"], tpassword=data["Password"])
        name = p[0].tname
    if len(p):
        s = SessionStore()
        s.set_expiry(160)
        s["ID"] = data["ID"]
        s["type"] = data["type"]
        s.save()
        s.clear_expired()
        result = HttpResponse(json.dumps({"name": name, "key": s.session_key}))
    return result


def logout(request):
    assert isinstance(request, HttpRequest)
    return HttpResponse("OK")


def view_course(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        s.set_expiry(160)
        s.save()
        courses = []
        if int(s["type"]) == 3:
            courses_id = Studentcourse.objects.filter(sid=int(s["ID"]))
            for course_id in courses_id:
                c = Course.objects.filter(cid=course_id.cid.cid).values()[0]
                c["endday"]=  c["endday"].strftime("%Y-%m-%d-%H")
                c["startday"] = c["startday"].strftime("%Y-%m-%d-%H")
                print(c)
                courses.append(c)
        elif int(s["type"]) == 2:
            courses = Course.objects.filter(teacherid=int(s["ID"])).values()
    except Exception as er:
        print(er.__class__,er)
        print(request.body)
        return HttpRequest("OO")

    return HttpResponse(json.dumps(courses))
