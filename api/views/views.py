from rest_framework import status
from pydantic import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from accounting.integration.accounting_model import ErpContact, ErpListMasterRequest, ErpMasterRequest
from accounting.integration.erp_api_client import ErpApiClient
from api.models.models import HbAppEntity
from api.models.serializers import HbAppEntitySerializer
from util.app_enum import Environment


class HbAppEntityViewSet(viewsets.ModelViewSet):
    queryset = HbAppEntity.objects.all()
    serializer_class = HbAppEntitySerializer


class MasterView(APIView):
    client = ErpApiClient(Environment.DEVELOPMENT)

    def post(self, request):
        try:
            if not request.data:
                return Response({"message": "Data is missing!"}, status=status.HTTP_400_BAD_REQUEST)

            erp_contacts = []
            errors = []
            for contact_data in request.data:
                try:
                    erp_contact = ErpContact(**contact_data)
                    erp_contacts.append(erp_contact)
                except ValidationError as e:
                    errors.append(e.errors())
                    # Check if there were any validation errors
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            master_data = ErpMasterRequest(contactList=erp_contacts)
            response = self.client.push_master(master_data)
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:

            erp_contact = self.client.get_master(
                erp_list_master=ErpListMasterRequest(page=1, limit=10, entityType='PARTY'))
            print(erp_contact)
            # Now perform some action with your 'invoice' object
            return Response(erp_contact, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)
