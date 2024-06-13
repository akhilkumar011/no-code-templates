import threading


class ThreadLocalData:
    THREAD_DATA = threading.local()


def set_thread_data(client_database, client_collection_suffix):
    ThreadLocalData.THREAD_DATA.client_database = client_database
    ThreadLocalData.THREAD_DATA.client_collection_suffix = client_collection_suffix


def get_thread_data(data_name):
    return getattr(ThreadLocalData.THREAD_DATA, data_name, None)
