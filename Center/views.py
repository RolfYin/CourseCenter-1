import datetime
import json
import multiprocessing
import urllib

from django.contrib.sessions.backends.db import SessionStore
from django.db import connection
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

# Create your views here.
from Center.models import *

globe_time = 360


def index(request):
    assert isinstance(request, HttpRequest)
    return HttpResponseRedirect("/eduadmin/index.html")


def download(request):
    assert isinstance(request, HttpRequest)
    try:
        key = request.GET["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        rc = Resource.objects.filter(cid=int(request.GET["cID"]), index=int(request.GET["index"]))[0]
        with open(rc.filepath, "r+b") as fd:
            data = fd.read()
        response = HttpResponse(data, content_type='application/octet-stream')
        response['Content-Disposition'] = "attachment; filename=\"{0}\"".format(
            urllib.parse.quote(rc.filename, safe='/[]'))
        return response
    except Exception as er:
        print("upload", er.__class__, er)
        print(request.body)
        return HttpResponse("", status=400)


rlock = multiprocessing.RLock()


def upload(request):
    global rlock
    assert isinstance(request, HttpRequest)
    try:
        rlock.acquire()
        key = request.POST["key"]
        s = SessionStore(session_key=key)
        s.set_expiry(globe_time)
        s.save()
        if int(s["type"] != 2):
            raise Exception
        cid = int(request.POST["cID"])
        filename = str(request.FILES["Filedata"])
        filepath = "Center/www/upload/" + filename
        category = "PPT"
        old = Resource.objects.filter(filename=filename)
        if len(old) > 0:
            index_ = old[0].index
        else:
            index_ = -1
        old_rc = list(Resource.objects.all().values())
        with open(filepath, "w+b") as fd:
            fd.write(request.FILES["Filedata"].file.read())
        with connection.cursor() as cur:
            cur.execute("insert into resource VALUES (%s,%s,%s,%s,%s)",
                        [cid, index_, filename, filepath, category])
        new_rc = []
        for rc in list(Resource.objects.all().values()):
            if rc not in old_rc:
                new_rc.append(rc)
        rlock.release()
        return HttpResponse(json.dumps(new_rc))
    except Exception as er:
        rlock.release()
        print("upload", er.__class__, er)
        return HttpResponse("",status=400)


def login(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        if int(data["type"]) == 3:
            p = Student.objects.filter(sid=int(data["ID"]), spassword=data["Password"])
            print(p)
            name = p[0].sname
        elif int(data["type"]) == 2:
            p = Teacher.objects.filter(tid=int(data["ID"]), tpassword=data["Password"])
            name = p[0].tname
        if len(p):
            s = SessionStore()
            s.set_expiry(globe_time)
            s["ID"] = data["ID"]
            s["type"] = data["type"]
            s.save()
            s.clear_expired()
            return HttpResponse(json.dumps({"name": name, "key": s.session_key}))
    except Exception as er:
        print("login", er.__class__, er)
        return HttpResponse("", status=400)


def logout(request):
    assert isinstance(request, HttpRequest)
    return HttpResponse("", status=400)


def view_course(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        courses = []
        if int(s["type"]) == 3:
            courses_id = Studentcourse.objects.filter(sid=int(s["ID"]))
            for course_id in courses_id:
                c = Course.objects.filter(cid=course_id.cid.cid).values()[0]
                c["endday"] = c["endday"].strftime("%Y-%m-%d-%H")
                c["startday"] = c["startday"].strftime("%Y-%m-%d-%H")
                c["tname"] = Teacher.objects.filter(tid=c["teacherid_id"])[0].tname
                courses.append(c)
        elif int(s["type"]) == 2:
            for course in Course.objects.filter(teacherid=int(s["ID"])).values():
                course["endday"] = course["endday"].strftime("%Y-%m-%d-%H")
                course["startday"] = course["startday"].strftime("%Y-%m-%d-%H")
                course["tname"] = Teacher.objects.filter(tid=course["teacherid_id"])[0].tname
                courses.append(course)
    except Exception as er:
        print("view_course", er.__class__, er)
        print(request.body)
        return HttpResponse("", status=400)
    return HttpResponse(json.dumps(courses))


def view_course_source(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        return HttpResponse(str(Resource.objects.filter(cid=int(data["cID"])).values()).replace("'", '"'))
    except Exception as er:
        print("view_course_source", er.__class__, er)
        return HttpResponse("", status=400)


def add_task(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        s = SessionStore(session_key=data["key"])
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        old = Task.objects.filter(name=data["TaskName"])
        if len(old):
            return HttpResponse({"index": old[0].index})
        cid = int(data["cID"])
        name = data["TaskName"]
        request = data["Description"]
        maxgrade = int(data["MaxPoint"])
        release = datetime.datetime.now()
        deadline = datetime.datetime.strptime(data["DeadLine"], "%Y-%m-%dT%H:%M")
        index_ = -1
        with connection.cursor() as cur:
            cur.execute("insert into task VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                        [cid, index_, name, request, release, deadline, "", maxgrade])
        old_task = Task.objects.filter(cid__cid=cid, name=name)[0]
        return HttpResponse(json.dumps({"index": old_task.index}))
    except Exception as er:
        print("add_task", er.__class__, er)
        return HttpResponse({"index": -1})


def task_upload(request):
    global rlock
    assert isinstance(request, HttpRequest)
    try:
        rlock.acquire()
        key = request.POST["key"]
        cID = int(request.POST["cID"])
        index_ = int(request.POST["index"])
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        if int(s["type"]) != 2:
            raise Exception
        filename = str(request.FILES["Filedata"])
        attachment = "Center/www/upload/" + filename
        with open(attachment, "w+b") as fd:
            fd.write(request.FILES["Filedata"].file.read())
        with connection.cursor() as cur:
            cur.execute("update task set Attachment=%s WHERE cID=%s and `Index`=%s;",
                        [attachment, cID, index_])
        rlock.release()
        return HttpResponse("OK")
    except Exception as er:
        rlock.release()
        print("task_upload", er.__class__, er)
        return HttpResponse("", status=400)


def view_task(request):
    assert isinstance(request, HttpRequest)
    try:
        data = request.GET
        key = data["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        tasks = []
        for task in Task.objects.filter(cid__cid=int(data["cID"])).values():
            task["release"] = task["release"].strftime("%Y-%m-%d %H:%M")
            task["deadline"] = task["deadline"].strftime("%Y-%m-%d %H:%M")
            tasks.append(task)
        return HttpResponse(json.dumps(tasks))
    except Exception as er:
        print("view_task", er.__class__, er)
        return HttpResponse("", status=400)


def view_finished_task(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        return HttpResponse(str(Resource.objects.filter(cid=int(data["cID"])).values()).replace("'", '"'))
    except Exception as er:
        print("view_finished_task", er.__class__, er)
        return HttpResponse("", status=400)


def view_taskinfo(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        task = Task.objects.filter(cid=int(data["cID"]), index=int(data["index"])).values()[0]
        task["release"] = task["release"].strftime("%Y-%m-%dT%H:%M")
        task["deadline"] = task["deadline"].strftime("%Y-%m-%dT%H:%M")
        print(task)
        return HttpResponse(json.dumps(task))
    except Exception as er:
        print("view_taskinfo", er.__class__, er)
        return HttpResponse("", status=400)


def view_submit(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        submitted = Worksubmit.objects.filter(cid=int(data["cID"]), sid=int(s["ID"]),
                                              taskindex=int(data["index"])).values()[0]
        submitted["submittime"] = submitted["submittime"].strftime("%Y-%m-%dT%H:%M")
        submitted = json.dumps(submitted)
        print(submitted)
        return HttpResponse(submitted)
    except Exception as er:
        print("view_submit", er.__class__, er)
        return HttpResponse("", status=400)


def view_worksubmit(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        submitted_works = Worksubmit.objects.filter(cid=int(data["cID"]), taskindex=int(data["Index"])).values()
        for submitted in submitted_works:
            submitted["submittime"] = submitted["submittime"].strftime("%Y-%m-%dT%H:%M")
            submitted["name"] = Student.objects.filter(sid=int(submitted["sid_id"]))[0].sname
            submitted["maxgrade"] = Task.objects.filter(cid=int(data["cID"]), index=int(data["Index"]))[0].maxgrade
        return HttpResponse(str(submitted_works).replace("'", '"'))
    except Exception as er:
        print("view_worksubmit", er.__class__, er)
        return HttpResponse("", status=400)


def submit_task(request):
    assert isinstance(request, HttpRequest)
    try:
        data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        submit_time = datetime.datetime.now()
        deadline = Task.objects.filter(cid=int(data["cID"]),index=int(data["index"]))[0].deadline
        if submit_time > deadline:
            raise Exception("beyond deadline!")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO worksubmit VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            [int(s["ID"]), int(data["cID"]), int(data["index"]), data["Description"], "unknown",
             submit_time, -1, ""])
        cursor.close()
        return HttpResponse("OK")
    except Exception as er:
        print("submit_task", er.__class__, er)
        return HttpResponse("", status=400)


def submit_upload(request):
    global rlock
    assert isinstance(request, HttpRequest)
    try:
        rlock.acquire()
        key = request.POST["key"]
        cID = request.POST["cID"]
        index_ = request.POST["index"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        if int(s["type"]) != 3:
            raise Exception
        submit_time = datetime.datetime.now()
        deadline = Task.objects.filter(cid=int(cID),index=int(index_))[0].deadline
        if submit_time > deadline:
            raise Exception("beyond deadline!")
        filename = str(request.FILES["Filedata"])
        file_path = "Center/www/upload/" + filename
        with connection.cursor() as cur:
            cur.execute("UPDATE worksubmit set FilePath=%s WHERE sID=%s and cID=%s and TaskIndex=%s",
                        [file_path, int(s["ID"]), int(cID), int(index_)])
        with open(file_path, "w+b") as fd:
            fd.write(request.FILES["Filedata"].file.read())
        rlock.release()
        return HttpResponse("OK")
    except Exception as er:
        rlock.release()
        print("submit_upload", er.__class__, er)
        return HttpResponse("", status=400)


def submit_download(request):
    global rlock
    assert isinstance(request, HttpRequest)
    try:
        rlock.acquire()
        key = request.GET["key"]
        cID = request.GET["cID"]
        sID = request.GET["sID"]
        index_ = request.GET["index"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        if int(s["type"]) != 2:
            raise Exception
        submit = Worksubmit.objects.filter(cid=int(cID), sid=int(sID), taskindex=int(index_))[0]
        with open(submit.filepath, "r+b") as fd:
            data = fd.read()
        response = HttpResponse(data, content_type='application/octet-stream')
        response['Content-Disposition'] = "attachment; filename=\"{0}\"".format(
            urllib.parse.quote(submit.filepath.rsplit("/", 1)[-1], safe='/[]'))
        rlock.release()
        return response
    except Exception as er:
        rlock.release()
        print("submit_upload", er.__class__, er)
        return HttpResponse("", status=400)


def task_download(request):
    assert isinstance(request, HttpRequest)
    try:
        data = request.GET
        # key = data["key"]
        # s = SessionStore(session_key=key)
        # if s["type"]:
        #     pass
        # s.set_expiry(globe_time)
        # s.save()
        task = Task.objects.filter(cid=int(data["cID"]), index=int(data["index"]))[0]
        with open(task.attachment, "r+b") as fd:
            data = fd.read()
        response = HttpResponse(data, content_type='application/octet-stream')
        response['Content-Disposition'] = "attachment; filename=\"{0}\"".format(
            urllib.parse.quote(task.attachment.rsplit("/", 1)[-1], safe='/[]'))
        return response
    except Exception as er:
        print("task_download", er.__class__, er)
        return HttpResponse("", status=400)


def score(request):
    assert isinstance(request, HttpRequest)
    try:
        data = data = json.loads(request.body.decode())
        key = data["key"]
        s = SessionStore(session_key=key)
        if s["type"]:
            pass
        s.set_expiry(globe_time)
        s.save()
        with connection.cursor() as cur:
            cur.execute("UPDATE worksubmit set Grade=%s,Comment=%s WHERE sID=%s and cID=%s and TaskIndex=%s",
                        [int(data["grade"]), data["comment"], int(data["sid"]), int(data["cid"]), int(data["index"])])
        return HttpResponse("OK")
    except Exception as er:
        print("task_download", er.__class__, er)
        return HttpResponse("", status=400)
