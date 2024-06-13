from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from accounting.data_utility.config import DATA_CODE
from accounting.data_utility.data_utility_accounting import *
from rest_framework.views import APIView
from rest_framework.response import Response

@csrf_exempt
@api_view(['POST', 'PUT', 'GET'])
def get_erp_utility_data(request, data_code=None,business_id=None):
    if request.method == "PUT":
        if data_code == DATA_CODE.TXN_COMMON_DATA_LINE:
            return save_or_update_common_data_line(request)
        elif data_code == DATA_CODE.TXN_JOURNAL_ENTRY:
            return save_or_update_txn_journal_entries(request)
        elif data_code == DATA_CODE.MASTER_CHART_ACCOUNTS:
            return save_or_update_master_coa(request)
        elif data_code == DATA_CODE.TXN_STOCK_MOVEMENT:
            return save_or_update_inventory_movements(request)
        else:
            return save_or_update_common_data(request)
    elif request.method == "POST":
        if data_code == DATA_CODE.TXN_COMMON_DATA_LINE:
            return fetch_common_data_line(request)
        elif data_code == DATA_CODE.TXN_JOURNAL_ENTRY:
            return fetch_txn_journal_entry(request)
        elif data_code == DATA_CODE.TXN_COMMON_DATA_LINE_WISE:
            return fetch_common_data_line_aggregate(request)
        elif data_code == DATA_CODE.TXN_COMMON_DATA_JOURNAL_ENTRY:
            return fetch_common_data_journal_entry_aggregate(request)
        elif data_code == DATA_CODE.TXN_STOCK_MOVEMENT:
            return fetch_txn_inventory_movements(request)
        elif data_code == DATA_CODE.TXN_STOCK_VALUATION_AVG:
            return fetch_inventory_valuation_avg(request)
        elif data_code == DATA_CODE.TXN_STOCK_VALUATION_FIFO:
            return fetch_inventory_valuation_fifo(request)
        else:
            return fetch_common_data(request)
    else:
        return fetch_common_data_url(request)
    
@api_view(['POST'])
def get_data_columns(request):
    return fetch_column_data(request)

class ConfigDataView(APIView):
    
    def common_method(self, request):
        try:
            business_id = request.query_params.get('businessId')
            query = {'businessId': business_id}
            config_data = HbErpDataUtilitySaveConfig.find(query)

            response_data = {
                "list": config_data, 
            }
            return JsonResponse(response_data, encoder=CustomJSONEncoder)
        except Exception as e:
            return Response({"status": "Error", "message": str(e)}, status=400)

    def post(self, request):
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            config_instance = HbErpDataUtilitySaveConfig(
                name= request_data.get("name"),
                businessId=request_data.get("businessId"),
                configData=request_data.get("data", [])
            )
            config_instance.save() 

            return Response({"status": "Success", "message": "Configuration saved successfully"})
        except Exception as e:
            return Response({"status": "Error", "message": str(e)}, status=400)

    def get(self, request):
        return self.common_method(request)