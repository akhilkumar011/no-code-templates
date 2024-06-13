import json
from datetime import datetime, date

import pandas as pd
import pytz
from bson import ObjectId

from accounting.data_utility.config import ACT_TXN_NAME, TXN_STATUS_ENUM
from util.mongo_orm.models import BaseModel


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, BaseModel):
            return obj.to_dict()
        return super().default(obj)


def process_document(document, valid_field_names):
    return [get_field_by_name(document.to_dict(), field) for field in valid_field_names]


def generate_csv_from_documents(documents, csv_filename, request_data):
    data_field = sorted(request_data.get('dataField', []), key=lambda x: x['orderNo'])
    field_dict = {}
    for field in data_field:
        field_dict[field['code']] = field['label']
    data_field_code = [field['code'] for field in data_field]
    df = pd.DataFrame(list(documents), columns=data_field_code)
    df.columns = [field_dict.get(col) for col in df.columns]
    df.to_csv(csv_filename, index=False, encoding='utf-8')


def get_field_by_name(txn_data, field):
    field_value = txn_data.get(field)
    if field == "txnType":
        field_value = ACT_TXN_NAME.get(str(field_value))
    elif field == "taxType":
        if str(field_value) == "ETAX":
            field_value = "Tax Exclusive"
        elif str(field_value) == "NTAX":
            field_value = "No Tax"
        elif str(field_value) == "ITAX":
            field_value = "Tax Inclusive"
    elif field == "status":
        field_value = TXN_STATUS_ENUM.get(str(field_value))

    if field_value is not None:
        if isinstance(field_value, date):
            return field_value.strftime("%d/%m/%Y")
        else:
            return str(field_value)
    else:
        return ""


def convert_timestamp_to_datetime(data, key_list):
    for key in key_list:
        if key in data and isinstance(data[key], int):
            utc_datetime = datetime.utcfromtimestamp(data[key] / 1000.0)
            local_timezone = pytz.timezone('Asia/Kolkata')
            data[key] = utc_datetime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return data
