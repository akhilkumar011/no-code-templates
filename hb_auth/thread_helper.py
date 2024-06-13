from accounting.data_utility.data_model import HbErpDataUtility
from hb_auth.thread_local_data import set_thread_data


def set_current_client_detail(business_id):
    data_utility: HbErpDataUtility = HbErpDataUtility.find_one({"businessId": business_id})
    if data_utility:
        set_thread_data(data_utility.mongoDatabase, data_utility.mongoCollectionSuffix)
