import json
import os
from datetime import timezone

from dateutil.relativedelta import relativedelta
from django.http import JsonResponse

from accounting.data_utility.data_model import *
from accounting.data_utility.inventory_valuation import call_inventory_fifo, call_inventory_avg
from hb_auth.thread_helper import set_current_client_detail
from util import common_function, S3_Client
from util.common_function import CustomJSONEncoder, convert_timestamp_to_datetime


def fetch_common_data(request):
    request_data = json.loads(request.body.decode('utf-8'))
    # Set Current Client Database detail
    set_current_client_detail(request_data.get("businessId"))
    # Define start and end dates for the filter
    query_filter = {
        "txnType": {"$in": list(request_data.get('docType'))},
        "isDeleted": False
    }
    if request_data.get('startDate') and request_data.get('endDate'):
        start_date = datetime.utcfromtimestamp(float(request_data.get('startDate')) / 1000).replace(tzinfo=timezone.utc)
        end_date = datetime.utcfromtimestamp(float(request_data.get('endDate')) / 1000).replace(tzinfo=timezone.utc)
        query_filter["txnDate"] = {"$gte": start_date, "$lte": end_date}

    if request_data.get('status'):
        query_filter["txnStatus"] = {"$in": list(request_data.get('status'))}

    page_size = request_data.get('pageSize')
    page_number = request_data.get('pageNumber')
    print(query_filter)
    total_count = 0
    if str(request_data.get("fetchType")) == "VIEW":
        total_count = HbTxnCommonData().count(query_filter)
    documents = HbTxnCommonData().find_by_limit(query_filter, page_number, page_size)
    return view_generate_csv_upload_s3(request_data, documents, total_count, page_size)


def fetch_common_data_line(request):
    request_data = json.loads(request.body.decode('utf-8'))
    # Set Current Client Database detail
    set_current_client_detail(request_data.get("businessId"))
    query_filter = {
        "txnType": {"$in": list(request_data.get('docType'))}
    }
    if request_data.get('startDate') and request_data.get('endDate'):
        start_date = datetime.utcfromtimestamp(float(request_data.get('startDate')) / 1000).replace(tzinfo=timezone.utc)
        end_date = datetime.utcfromtimestamp(float(request_data.get('endDate')) / 1000).replace(tzinfo=timezone.utc)
        query_filter["txnDate"] = {"$gte": start_date, "$lte": end_date}

    page_size = request_data.get('pageSize')
    page_number = request_data.get('pageNumber')
    total_count = 0
    if str(request_data.get("fetchType")) == "VIEW":
        total_count = HbTxnCommonDataLine().count(query_filter)
    documents = HbTxnCommonDataLine().find_by_limit(query_filter, page_number, page_size)
    return view_generate_csv_upload_s3(request_data, documents, total_count, page_size)


def fetch_common_data_line_aggregate(request):
    request_data = json.loads(request.body.decode('utf-8'))
    # Set Current Client Database detail
    set_current_client_detail(request_data.get("businessId"))
    query_filter = {
        "txnType": {"$in": list(request_data.get('docType'))},
        "isDeleted": False
    }
    if request_data.get('startDate') and request_data.get('endDate'):
        start_date = datetime.utcfromtimestamp(float(request_data.get('startDate')) / 1000).replace(tzinfo=timezone.utc)
        end_date = datetime.utcfromtimestamp(float(request_data.get('endDate')) / 1000).replace(tzinfo=timezone.utc)
        query_filter["txnDate"] = {"$gte": start_date, "$lte": end_date}

    page_size = request_data.get('pageSize')
    page_number = request_data.get('pageNumber')
    total_count = 0
    if str(request_data.get("fetchType")) == "VIEW":
        total_count = HbTxnCommonDataLine().count(query_filter)
    documents: list[HbTxnCommonDataLine] = HbTxnCommonDataLine().find_by_limit(query_filter, page_number, page_size)
    hb_txn_wise = []
    for entry in documents:
        data: HbTxnCommonData = HbTxnCommonData().find_one({"txnId": entry.txnId})
        if data:
            hb_txn_wise.append(HbTxnItemDetail(**{
                key: entry.__dict__[key] for key in entry.__dict__ if
                key not in ['txn_common_data', '_id', 'client', 'collection_name', 'txnId', 'txnDate', 'nativeAmount',
                            'txnType', 'updatedAt', 'updatedBy', 'updatedByName', 'updatedByUser', 'createdAt',
                            'createdBy', 'createdByUser', 'createdByName', 'contactId', 'branchId', 'isDeleted']
            }, **data.to_dict()))

    return view_generate_csv_upload_s3(request_data, hb_txn_wise, total_count, page_size)


def fetch_common_data_journal_entry_aggregate(request):
    request_data = json.loads(request.body.decode('utf-8'))
    # Set Current Client Database detail
    set_current_client_detail(request_data.get("businessId"))
    query_filter = {
        "txnType": {"$in": list(request_data.get('docType'))},
        "isDeleted": False
    }
    if request_data.get('startDate') and request_data.get('endDate'):
        start_date = datetime.utcfromtimestamp(float(request_data.get('startDate')) / 1000).replace(tzinfo=timezone.utc)
        end_date = datetime.utcfromtimestamp(float(request_data.get('endDate')) / 1000).replace(tzinfo=timezone.utc)
        query_filter["txnDate"] = {"$gte": start_date, "$lte": end_date}

    page_size = request_data.get('pageSize')
    page_number = request_data.get('pageNumber')
    total_count = 0
    if str(request_data.get("fetchType")) == "VIEW":
        total_count = HbTxnJournalEntry().count(query_filter)
    documents: list[HbTxnJournalEntry] = HbTxnJournalEntry().find_by_limit(query_filter, page_number, page_size)
    hb_txn_wise = []
    for entry in documents:
        data: HbTxnCommonData = HbTxnCommonData().find_one({"txnId": entry.txnId})
        if data:
            hb_txn_wise.append(HbTxnItemDetail(**{
                key: entry.__dict__[key] for key in entry.__dict__ if
                key not in ['txn_common_data', '_id', 'client', 'collection_name', 'txnId', 'txnDate', 'nativeAmount',
                            'txnType', 'updatedAt', 'updatedBy', 'updatedByName', 'updatedByUser', 'createdAt',
                            'createdBy', 'createdByUser', 'createdByName', 'contactId', 'branchId', 'isDeleted']
            }, **data.to_dict()))
    return view_generate_csv_upload_s3(request_data, hb_txn_wise, total_count, page_size)


def fetch_txn_journal_entry(request):
    request_data = json.loads(request.body.decode('utf-8'))
    # Set Current Client Database detail
    set_current_client_detail(request_data.get("businessId"))
    query_filter = {
        "txnType": {"$in": list(request_data.get('docType'))},
        "isDeleted": False
    }
    if request_data.get('startDate') and request_data.get('endDate'):
        start_date = datetime.utcfromtimestamp(float(request_data.get('startDate')) / 1000).replace(tzinfo=timezone.utc)
        end_date = datetime.utcfromtimestamp(float(request_data.get('endDate')) / 1000).replace(tzinfo=timezone.utc)
        query_filter["txnDate"] = {"$gte": start_date, "$lte": end_date}
    if request_data.get('accountIds'):
        query_filter["accountId"] = {"$in": list(request_data.get('accountIds'))}
    page_size = request_data.get('pageSize')
    page_number = request_data.get('pageNumber')
    total_count = 0
    if str(request_data.get("fetchType")) == "VIEW":
        total_count = HbTxnJournalEntry().count(query_filter)
    print(query_filter)
    documents = HbTxnJournalEntry().find_by_limit(query_filter, page_number, page_size)
    return view_generate_csv_upload_s3(request_data, documents, total_count, page_size)


def fetch_txn_inventory_movements(request):
    request_data = json.loads(request.body.decode('utf-8'))
    # Set Current Client Database detail
    set_current_client_detail(request_data.get("businessId"))
    query_filter = {
        "status": True
    }
    if request_data.get('docType'):
        query_filter["txnType"] = {"$in": list(request_data.get('docType'))}

    if request_data.get('startDate') and request_data.get('endDate'):
        start_date = datetime.utcfromtimestamp(float(request_data.get('startDate')) / 1000).replace(tzinfo=timezone.utc)
        end_date = datetime.utcfromtimestamp(float(request_data.get('endDate')) / 1000).replace(tzinfo=timezone.utc)
        query_filter["txnDate"] = {"$gte": start_date, "$lte": end_date}

    if request_data.get('itemIds'):
        query_filter["itemIds"] = {"$in": list(request_data.get('itemIds'))}

    page_size = request_data.get('pageSize')
    page_number = request_data.get('pageNumber')
    total_count = 0
    if str(request_data.get("fetchType")) == "VIEW":
        total_count = HbTxnInventoryMovements().count(query_filter)
    print(query_filter)
    documents = HbTxnInventoryMovements().find_by_limit(query_filter, page_number, page_size, sort=[("txnDate", 1)])
    hb_txn_wise = []
    for entry in documents:
        data: HbTxnCommonData = HbTxnCommonData().find_one({"txnId": entry.txnId})
        if data:
            hb_txn_wise.append(HbTxnInventoryMovementDetail(**{
                key: entry.__dict__[key] for key in entry.__dict__ if
                key not in ['txn_common_data', '_id', 'client', 'collection_name', 'txnId', 'txnDate', 'nativeAmount',
                            'txnType', 'updatedAt', 'updatedBy', 'updatedByName', 'updatedByUser', 'createdAt',
                            'createdBy', 'createdByUser', 'createdByName', 'contactId', 'branchId', 'isDeleted',
                            'status', 'txnStatus',
                            'reference']
            }, **data.to_dict()))
    return view_generate_csv_upload_s3(request_data, hb_txn_wise, total_count, page_size)


def fetch_inventory_valuation_avg(request):
    request_data = json.loads(request.body.decode('utf-8'))
    # Set Current Client Database detail
    set_current_client_detail(request_data.get("businessId"))
    start_date = datetime.now() - relativedelta(years=1)
    end_date = datetime.now()
    if request_data.get('startDate') and request_data.get('endDate'):
        start_date = datetime.utcfromtimestamp(float(request_data.get('startDate')) / 1000).replace(tzinfo=timezone.utc)
        end_date = datetime.utcfromtimestamp(float(request_data.get('endDate')) / 1000).replace(tzinfo=timezone.utc)
    return view_generate_csv_upload_s3(request_data, call_inventory_avg(start_date, end_date), 0, 100)


def fetch_inventory_valuation_fifo(request):
    request_data = json.loads(request.body.decode('utf-8'))
    # Set Current Client Database detail
    set_current_client_detail(request_data.get("businessId"))
    start_date = datetime.now() - relativedelta(years=1)
    end_date = datetime.now()
    if request_data.get('startDate') and request_data.get('endDate'):
        start_date = datetime.utcfromtimestamp(float(request_data.get('startDate')) / 1000).replace(tzinfo=timezone.utc)
        end_date = datetime.utcfromtimestamp(float(request_data.get('endDate')) / 1000).replace(tzinfo=timezone.utc)
    return view_generate_csv_upload_s3(request_data, call_inventory_fifo(start_date, end_date), 0, 100)


def view_generate_csv_upload_s3(request_data, documents, total_count, page_size):
    # Close the MongoDB connection
    if str(request_data.get("fetchType")) == "VIEW":
        total_pages = -(-total_count // page_size)
        response_data = {
            "list": documents,
            "pageCount": total_pages,
            "totalRowCount": total_count,
        }
        return JsonResponse(response_data, encoder=CustomJSONEncoder)
    else:
        # Generate a timestamp for the file name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Append the timestamp to the file name
        file_name = f'data_file_{timestamp}.csv'
        data = HbExportUtilityDocument()
        data.docId = str(request_data.get('requestId'))
        data.progress = 0
        data.estimatedTime = 5
        data.status = False
        save_or_update_file_info(data)
        common_function.generate_csv_from_documents(documents, file_name, request_data)
        with open(file_name, 'rb') as file_obj:
            s3_bucket, s3_key = S3_Client.upload_file_local(file_obj, file_name)
        data.s3Key = s3_key
        data.s3Bucket = s3_bucket
        data.status = True
        save_or_update_file_info(data)
        os.remove(file_name)
    return JsonResponse({"status": "SuccessFully"})


def save_or_update_file_info(data):
    query = {"docId": data.docId}
    hb_export = data.find_one(query)
    if hb_export:
        data.update_by_query(query)
    else:
        data.save()


def fetch_common_data_url(request):
    request_id = request.GET.get('requestId')
    existing_document: HbExportUtilityDocument = HbExportUtilityDocument().find_one({"docId": request_id})
    if existing_document and existing_document.status:
        return JsonResponse(
            {"data": existing_document,
             "url": S3_Client.download_file(existing_document.s3Key, existing_document.s3Bucket)},
            encoder=CustomJSONEncoder)
    else:
        return JsonResponse({"data": existing_document, "url": ""}, encoder=CustomJSONEncoder)


def save_or_update_common_data(request):
    set_current_client_detail(request.GET.get('businessId'))
    txn_common_data_list = json.loads(request.body.decode('utf-8'))
    hb_txn_list = [HbTxnCommonData(**convert_timestamp_to_datetime(data,
                                                                   ['dueDate', 'txnDate', 'createdAt', 'updatedAt',
                                                                    'ackDate', 'cancelDate', 'billOfEntryDate',
                                                                    'challanDate'])) for data in txn_common_data_list]
    for hb_txn in hb_txn_list:
        query = {"txnId": hb_txn.txnId}
        existing_document = hb_txn.find_one(query)
        if existing_document:
            hb_txn.update_by_query(query)
        else:
            hb_txn.save()
    return JsonResponse({"status": "SuccessFully"})


def save_or_update_common_data_line(request):
    set_current_client_detail(request.GET.get('businessId'))
    txn_common_data_line_list = json.loads(request.body.decode('utf-8'))
    hb_txn_line_list = [
        HbTxnCommonDataLine(**convert_timestamp_to_datetime(data, ['updatedAt', 'txnDate', 'createdAt'])) for data
        in txn_common_data_line_list]
    HbTxnCommonDataLine().delete_many_by_query({
        "txnId": {"$in": [entry.txnId for entry in hb_txn_line_list]}
    })
    for hb_txn_line in hb_txn_line_list:
        query = {"lineId": hb_txn_line.lineId}
        existing_document = hb_txn_line.find_one(query)
        if existing_document:
            hb_txn_line.update_by_query(query)
        else:
            hb_txn_line.save()
    return JsonResponse({"status": "SuccessFully"})


def save_or_update_txn_journal_entries(request):
    set_current_client_detail(request.GET.get('businessId'))
    txn_journal_entries_list = json.loads(request.body.decode('utf-8'))
    journal_entries_list = [HbTxnJournalEntry(**convert_timestamp_to_datetime(data, ['txnDate'])) for data in
                            txn_journal_entries_list]
    HbTxnJournalEntry().delete_many_by_query({
        "txnId": {"$in": [entry.txnId for entry in journal_entries_list]}
    })
    for journal in journal_entries_list:
        query = {"journalId": journal.journalId}
        existing_document: HbTxnJournalEntry = journal.find_one(query)
        if existing_document:
            journal.update_by_query(query)
        else:
            journal.save()
    return JsonResponse({"status": "Successfully"})


def save_or_update_master_coa(request):
    set_current_client_detail(request.GET.get('businessId'))
    coa_list = json.loads(request.body.decode('utf-8'))
    coa_entries_list = [
        HbMasterChartOfAccount(**convert_timestamp_to_datetime(data, ['updatedAt', 'openingDate', 'createdAt'])) for
        data in
        coa_list]
    for coa in coa_entries_list:
        query = {"accountId": coa.accountId}
        existing_document = coa.find_one(query)
        if existing_document:
            coa.update_by_query(query)
        else:
            coa.save()
    return JsonResponse({"status": "Successfully"})


def save_or_update_inventory_movements(request):
    set_current_client_detail(request.GET.get('businessId'))
    inventory_txn_list = json.loads(request.body.decode('utf-8'))
    coa_entries_list = [
        HbTxnInventoryMovements(**convert_timestamp_to_datetime(data, ['updatedAt', 'txnDate', 'createdAt'])) for
        data in
        inventory_txn_list]
    HbTxnInventoryMovements().delete_many_by_query({
        "txnId": {"$in": [entry.txnId for entry in coa_entries_list]}
    })
    for inventory_txn in coa_entries_list:
        query = {"adjId": inventory_txn.adjId}
        inventory_txn.status = True if inventory_txn.status == 1 else False
        existing_document = inventory_txn.find_one(query)
        if existing_document:
            inventory_txn.update_by_query(query)
        else:
            inventory_txn.save()
    return JsonResponse({"status": "Successfully"})


def fetch_column_data(request):
    request_data = json.loads(request.body.decode('utf-8'))
    # Define start and end dates for the filter
    query_filter = {
        "dataCode": request_data.get('dataCode'),
        "dataType": {"$in": list(request_data.get('dataType'))},
    }

    return JsonResponse(
        {"config": HbExportUtilityConfigData().find(query_filter,
                                                    sort=[("orderNo", 1)]) + HbExportUtilityConfigData().find(
            {"dataType": "TXN_STATUS"}, sort=[("label", 1)])},
        encoder=CustomJSONEncoder)
