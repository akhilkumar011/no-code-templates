from dataclasses import dataclass, asdict
from datetime import datetime

from util.mongo_orm.repository import BaseRepository

exclude_fields = ['collection_name', 'client']


@dataclass
class BaseModel:
    collection_name: str = None
    client: bool = False

    def save(self):
        repository = BaseRepository(self.collection_name, self.__class__, client=self.client)
        return repository.inert_one(self.__dict__)

    def update(self):
        repository = BaseRepository(self.collection_name, self.__class__, client=self.client)
        return repository.update_one(self.__dict__)

    def update_by_query(self, query):
        repository = BaseRepository(self.collection_name, self.__class__, client=self.client)
        return repository.update_by_query(query, self.__dict__)

    def update_by_query_data(self, query, data):
        repository = BaseRepository(self.collection_name, self.__class__, client=self.client)
        return repository.update_by_query_data(query, data)

    def delete_by_id(self, document_id):
        repository = BaseRepository(self.collection_name, self.__class__, client=self.client)
        return repository.delete_by_id(document_id)

    def delete_by_query(self, query):
        repository = BaseRepository(self.collection_name, self.__class__, client=self.client)
        return repository.delete_by_query(query)

    def delete_many_by_query(self, query):
        repository = BaseRepository(self.collection_name, self.__class__, client=self.client)
        return repository.delete_many_by_query(query)

    @classmethod
    def find(cls, query=None, sort=None):
        repository = BaseRepository(cls.collection_name, cls, client=cls.client)
        return repository.find_all(query, sort)

    @classmethod
    def find_by_limit(cls, query=None, page=1, per_page=10, sort=None):
        repository = BaseRepository(cls.collection_name, cls, client=cls.client)
        return repository.find_by_limit(query, page, per_page, sort)

    @classmethod
    def find_one(cls, query):
        repository = BaseRepository(cls.collection_name, cls, client=cls.client)
        return repository.find_one(query)

    @classmethod
    def find_by_id(cls, object_id):
        repository = BaseRepository(cls.collection_name, cls, client=cls.client)
        return repository.find_by_id(object_id)

    @classmethod
    def aggregate(cls, pipeline, query=None, page=1, per_page=10, sort_by=None):
        repository = BaseRepository(cls.collection_name, cls, client=cls.client)
        return repository.aggregate(pipeline, query, page, per_page, sort_by)

    @classmethod
    def aggregate_raw(cls, pipeline):
        repository = BaseRepository(cls.collection_name, cls, client=cls.client)
        return repository.aggregate_raw(pipeline)

    @classmethod
    def aggregate_count(cls, pipeline, query=None):
        repository = BaseRepository(cls.collection_name, cls, client=cls.client)
        return repository.aggregate_count(pipeline, query)

    @classmethod
    def count(cls, query):
        repository = BaseRepository(cls.collection_name, cls, client=cls.client)
        return repository.count_documents(query)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            setattr(instance, key, value)
        return instance


def convert_to_dict(obj, object_flag=False):
    """
    Recursively converts an object to a dictionary.
    """
    if object_flag:
        # Convert HbTxnCommonData attributes to a dictionary
        return {key: convert_to_dict(value) if hasattr(value, '__dict__') else value for key, value in
                obj.__dict__.items()}
    elif isinstance(obj, list):
        # Convert each item in the list to a dictionary
        return [convert_to_dict(item) for item in obj]
    elif isinstance(obj, datetime):
        # Convert datetime object to ISO format string
        return obj.isoformat()
    else:
        return obj
