# connection.py
import pymongo
from django.conf import settings

from hb_auth.thread_local_data import get_thread_data


class MongoDBConnection:
    _instance_main = None
    _instance_act = None
    stage = getattr(settings, 'STAGE')
    main_db_uri = getattr(settings, 'DB_URI')
    main_database = getattr(settings, 'DB_NAME')
    client_db_uri = getattr(settings, 'ACT_DB_URI')
    client_database = getattr(settings, 'ACT_DB_NAME')

    def __new__(cls, *args, **kwargs):
        # Create a new main instance only if it doesn't exist
        if 'client' in kwargs and kwargs['client']:
            if not cls._instance_act:
                cls._instance_act = super(MongoDBConnection, cls).__new__(cls)
                return cls._instance_act
            else:
                return cls._instance_act
        else:
            if not cls._instance_main:
                cls._instance_main = super(MongoDBConnection, cls).__new__(cls)
                return cls._instance_main
            else:
                return cls._instance_main

    def __init__(self, client=False):
        if not hasattr(self, 'initialized'):
            self.act_client = None
            self.main_client = None
            self.db_act = None
            self.db_main = None
            if not self.act_client and client:
                print("CONNECTING=> self.client_db_uri", self.client_db_uri)
                if self.stage != 'TEST':
                    self.act_client = pymongo.MongoClient(self.client_db_uri, tls=True,
                                                          tlsAllowInvalidCertificates=True)
                else:
                    self.act_client = pymongo.MongoClient(self.client_db_uri)
                if get_thread_data("client_database"):
                    self.db_act = self.act_client[get_thread_data("client_database")]
                else:
                    self.db_act = self.act_client[self.client_database]

            if not self.main_client:
                print("CONNECTING=> self.main_db_uri", self.main_db_uri)
                if self.stage != 'TEST':
                    self.main_client = pymongo.MongoClient(self.main_db_uri, tls=True,
                                                           tlsAllowInvalidCertificates=True)
                else:
                    self.main_client = pymongo.MongoClient(self.main_db_uri)
                self.db_main = self.main_client[self.main_database]
            self.initialized = True

    @classmethod
    def get_collection(cls, collection_name, client=False):
        if client:
            if get_thread_data("client_collection_suffix"):
                return cls._instance_act.db_act[collection_name + get_thread_data("client_collection_suffix")]
            else:
                return cls._instance_act.db_act[collection_name]
        else:
            return cls._instance_main.db_main[collection_name]
