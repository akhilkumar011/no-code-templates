from accounting.integration.config import *
from util.request_client import RequestClient


class ErpApiClient:
    def __init__(self, env=Environment.DEVELOPMENT):
        self.client = RequestClient(BASE_URLS[env], headers)

    def get_master(self, erp_list_master):
        """
        Push contact data_utility to the ERP system.
        """
        response = self.client.post(LIST_MASTER, data=erp_list_master.dict())
        return response

    def push_master(self, master):
        """
        Push contact data_utility to the ERP system.
        """
        response = self.client.post(ADD_MASTER, data=master.dict())
        return response

    def get_transaction(self, erp_list_transaction):
        """
        Push contact data_utility to the ERP system.
        """
        response = self.client.post(LIST_TRANSACTION, data=erp_list_transaction.dict())
        return response

    def push_transaction(self, transaction):
        """
        Push invoice data_utility to the ERP system.
        """
        response = self.client.post(ADD_TRANSACTION, data=transaction.dict())
        return response
