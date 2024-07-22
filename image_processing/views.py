from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import json
import datetime
import random
import string
import base64


def index(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Escaneo", "route": "scanner.index"},
    ]
    viewData["api_key"] = settings.API_KEY
    viewData["ip_server"] = settings.IP_SERVER
    return render(request, 'image_processing/scanner.html', {"viewData": viewData})


def test(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Escaneo", "route": "scanner.index"},
    ]
    viewData["api_key"] = settings.API_KEY
    viewData["ip_server"] = settings.IP_SERVER
    return render(request, 'image_processing/scanner_test.html', {"viewData": viewData})


def save(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        image_data = body['frame']
        base64_str = image_data.split(";base64,")[1]
        image_data_decoded = base64.b64decode(base64_str)

        fs = FileSystemStorage()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        random_text = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        file_name = f"{current_date}-{random_text}.png"
        fs.save('scanned_pics/' + file_name, ContentFile(image_data_decoded))

    data = {
        'status': 'success'
    }
    return JsonResponse(data)
