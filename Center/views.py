import json
import multiprocessing

from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

# Create your views here.
from Center.models import *


def index(request):
    assert isinstance(request, HttpRequest)
    return HttpResponseRedirect("/eduadmin/index.html")


def download(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        s.set_expiry(160)
        s.save()
        rc = Resource.objects.filter(cid=int(data["cID"]), index=int(data["index"]))[0]
        with open(rc.filepath, "r+b") as fd:
            data = fd.read()
        response = HttpResponse(data, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(rc.filename)
        return response
    except Exception as er:
        print(er.__class__, er)
        print(request.body)
        return HttpResponse("{}")


rlock = multiprocessing.RLock()


def upload(request):
    global rlock
    assert isinstance(request, HttpRequest)
    try:
        rlock.acquire()
        key = request.POST["key"]
        s = SessionStore(session_key=key)
        s.set_expiry(160)
        s.save()
        rc = Resource()
        rc.cid = Course.objects.filter(cid=int(request.POST["cID"]))[0]
        filename = str(request.FILES["Filedata"])
        rc.filename = filename
        rc.filepath = "Center/www/upload/" + filename
        rc.category = "PPT"
        old = Resource.objects.filter(filename=filename)
        if len(old) > 0:
            rc.index = old[0].index
        else:
            rc.index = -1
        old_rc = list(Resource.objects.all().values())
        with open(rc.filepath, "w+b") as fd:
            fd.write(request.FILES["Filedata"].file.read())
        rc.save()
        new_rc = []

        for rc in list(Resource.objects.all().values()):
            if rc not in old_rc:
                new_rc.append(rc)
        rlock.release()
        return HttpResponse(json.dumps(new_rc))
    except Exception as er:
        print(er.__class__, er)
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
            for course in Course.objects.filter(teacherid=int(s["ID"])).values():
                course["endday"] = course["endday"].strftime("%Y-%m-%d-%H")
                course["startday"] = course["startday"].strftime("%Y-%m-%d-%H")
                courses.append(course)
    except Exception as er:
        print(er.__class__, er)
        print(request.body)
        return HttpResponse("{}")
    return HttpResponse(json.dumps(courses))


def view_course_source(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        s.set_expiry(160)
        s.save()
        return HttpResponse(str(Resource.objects.filter(cid=int(data["cID"])).values()).replace("'", '"'))
    except Exception as er:
        print(er.__class__, er)
        return HttpResponse("{}")


def add_task(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        s.set_expiry(160)
        s.save()
        return HttpResponse(str(Resource.objects.filter(cid=int(data["cID"])).values()).replace("'", '"'))
    except Exception as er:
        print(er.__class__, er)
        return HttpResponse("{}")
