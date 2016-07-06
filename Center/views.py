# -encoding=utf-8
import io
import json

from django.contrib.sessions.backends.db import SessionStore
from django.core import serializers
from django.http import HttpResponse, HttpRequest

# Create your views here.
from Center.models import *


def download(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        s.set_expiry(160)
        s.save()
        rc = Resource.objects.filter(cid=int(data["cID"]))[0]
        with open(rc.filepath, "r+b") as fd:
            data = fd.read()
        response = HttpResponse(data, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(rc.filename)
        return response
    except Exception as er:
        print(er.__class__, er)
        print(request.body)
        return HttpResponse("{}")


def upload(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        s.set_expiry(160)
        s.save()
        filename = request.FILES["Filedata"]
        rc = Resource()
        rc.cid = int(data["cID"])
        rc.filename = filename
        rc.filepath = "Center/www/uplaod/" + filename
        rc.category = "PPT"
        rc.index = 0
        rc.save()
        old_rc = set(Resource.objects.filter(cid=rc.cid).values())
        assert isinstance(request.FILES["Filedata"].file, io.BytesIO)
        with open(rc.filepath, "w+b") as fd:
            fd.write(request.FILES["Filedata"].file.read())
        new_rc = set(Resource.objects.filter(cid=rc.cid).values()) - old_rc
        return HttpResponse(json.dumps(list(new_rc)))
    except Exception as er:
        print(er.__class__, er)
        print(request.body)
        return HttpResponse("[]")


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
                c["endday"] = c["endday"].strftime("%Y-%m-%d-%H")
                c["startday"] = c["startday"].strftime("%Y-%m-%d-%H")
                print(c)
                courses.append(c)
        elif int(s["type"]) == 2:
            courses = Course.objects.filter(teacherid=int(s["ID"]))
    except Exception as er:
        print(er.__class__, er)
        print(request.body)
        return HttpResponse("{}")

    return HttpResponse(serializers.serialize("json", courses))


def view_course_source(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        s.set_expiry(160)
        s.save()
        rcs = serializers.serialize("json", Resource.objects.filter(cid=int(data["cID"])))
        return HttpResponse(rcs)
    except Exception as er:
        print(er.__class__, er)
        return HttpResponse("{}")
