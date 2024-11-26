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
from accounts.models import ScanningStatistics
import logging

logger = logging.getLogger(__name__)


def index(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "Scanner", "route": "scanner.index"},
    ]
    viewData["api_key"] = settings.API_KEY
    viewData["ip_server"] = settings.IP_SERVER
    return render(request, 'image_processing/scanner.html', {"viewData": viewData})


def test(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "Scanner", "route": "scanner.index"},
    ]
    viewData["api_key"] = settings.API_KEY
    viewData["ip_server"] = settings.IP_SERVER
    return render(request, 'image_processing/scanner_test.html', {"viewData": viewData})


def save(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        image_data = body['frame']
        prediction = str(body.get('prediction', '-1'))

        # Guardar la imagen
        base64_str = image_data.split(";base64,")[1]
        image_data_decoded = base64.b64decode(base64_str)
        fs = FileSystemStorage()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        random_text = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        file_name = f"{current_date}-{random_text}.png"
        fs.save('scanned_pics/' + file_name, ContentFile(image_data_decoded))

        # Map prediction to waste type
        WASTE_TYPE_MAPPING = {
            '-1': 'UNCERTAIN',
            '0': 'BOTTLE',
            '1': 'PRINTED_PACKAGING',
            '2': 'CONTAINER',
            '3': 'CAN',
            '4': 'ORGANIC',
            '5': 'OTHER',
            '6': 'NON_RECYCLABLE_PAPER',
            '7': 'PAPERS'
        }

        waste_type = WASTE_TYPE_MAPPING.get(prediction, 'UNCERTAIN')

        # Determine bin type
        if prediction in ['-1', '5']:
            bin_type = 'BLACK'
        elif prediction == '6':
            bin_type = 'GREEN'
        else:
            bin_type = 'WHITE'

        CO2_SAVINGS = {
            'BOTTLE': 0.0833,
            'PRINTED_PACKAGING': 0.0458,
            'CONTAINER': 0.0833,
            'CAN': 0.113,
            'ORGANIC': 0.091,
            'PAPERS': 0.0458,
            'OTHER': 0,
            'NON_RECYCLABLE_PAPER': 0,
            'UNCERTAIN': 0
        }

        EXPERIENCE_POINTS = {
            'BOTTLE': 10,
            'PRINTED_PACKAGING': 5,
            'CONTAINER': 10,
            'CAN': 15,
            'ORGANIC': 20,
            'PAPERS': 5,
            'OTHER': 0,
            'NON_RECYCLABLE_PAPER': 0,
            'UNCERTAIN': 0
        }

        co2_saved = CO2_SAVINGS.get(waste_type, 0)
        experience = EXPERIENCE_POINTS.get(waste_type, 0)

        if request.user.is_authenticated:
            ScanningStatistics.objects.create(
                waste_type=waste_type,
                bin_type=bin_type,
                user=request.user,
                co2_saved=co2_saved,
                experience=experience
            )

    data = {
        'status': 'success',
        'co2_saved': co2_saved,
        'experience': experience
    }
    return JsonResponse(data)
