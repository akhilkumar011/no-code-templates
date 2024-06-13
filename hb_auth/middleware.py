import uuid

from django.http import HttpResponse

from .models import ClientDetail
from HbERPUtility.urls import EXCLUDED_PATHS


class ClientDetailAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path is in the excluded paths
        # if not any(request.path.startswith(path) for path in EXCLUDED_PATHS):
        #     apiKey = request.headers.get('x-api-key')
        #     if not apiKey:
        #         return HttpResponse("Missing API key", status=400)

        #     try:
        #         key = ClientDetail.objects.get(apiKey=uuid.UUID(apiKey))
        #     except ClientDetail.DoesNotExist:
        #         return HttpResponse("Invalid API key", status=401)

        #     # Attach the key to the request if you want to access it in your views
        #     request.api_key = key.apiKey

        response = self.get_response(request)
        return response
