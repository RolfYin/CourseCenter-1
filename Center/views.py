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
    with open("test.jpg", "w+b") as fd:
        fd.write(request.body)
    return HttpResponse("OK")
