import logging

from bson import ObjectId

from util.mongo_orm.connection import MongoDBConnection

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pymongo')
logger.setLevel(logging.DEBUG)

exclude_keys = ['client', 'collection_name']


class BaseRepository:
    def __init__(self, collection_name, model_class, client=False):
        self.connection = MongoDBConnection(client=client)
        self.collection = MongoDBConnection.get_collection(collection_name, client=client)
        self.model_class = model_class

    def inert_one(self, data):
        result = self.collection.insert_one(data)
        logger.info(f"Object inserted with ID: {result.inserted_id}")
        return result.inserted_id

    def inert_many(self, data):
        result = self.collection.insert_many(data)
        return result.inserted_ids

    def update_one(self, data):
        self.collection.update_one({'_id': data['_id']}, {'$set': data})
        logger.info(f"Object updated for criteria: {'_id': data['_id']}")
        return data['_id']

    def update_by_query(self, query, data):
        # Exclude the '_id' field from the update
        update_data = {key: value for key, value in data.items() if key != '_id'}
        self.collection.update_one(query, {'$set': update_data})
        logger.info(f"Object updated for criteria: query")
        return query

    def update_by_query_data(self, query, update_data):
        # Exclude the '_id' field from the update
        self.collection.update_many(query, update_data)
        logger.info(f"Object updated for criteria: query")
        return query

    def delete_by_id(self, document_id):
        result = self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count

    def delete_by_query(self, query):
        result = self.collection.delete_one(query)
        return result.deleted_count

    def delete_many_by_query(self, query):
        result = self.collection.delete_many(query)
        return result.deleted_count

    def find_all(self, query=None, sort=None):
        documents = self.collection.find(query) if query else self.collection.find()
        if sort:
            documents = documents.sort(sort)
        return [self.model_class(**doc) for doc in documents]

    def find_by_limit(self, query=None, page=1, per_page=10, sort=None):
        skip_count = (page - 1) * per_page
        documents = self.collection.find(query).skip(skip_count).limit(per_page)
        if sort:
            documents = documents.sort(sort)
        return [self.model_class(**doc) for doc in documents]

    def find_one(self, query):
        document = self.collection.find_one(query)
        return self.model_class(**document) if document else None

    def find_by_id(self, object_id):
        document = self.collection.find_one({'_id': ObjectId(object_id)})
        return self.model_class(**document) if document else None

    def aggregate(self, pipeline, query=None, page=1, per_page=10, sort_by=None):
        if query:
            # match_stage = {'$match': query}
            pipeline[0]["$lookup"]["pipeline"].append({"$match": query})
            # pipeline.append(match_stage)

        # Add $sort stage based on sort_by
        if sort_by:
            sort_stage = {'$sort': sort_by}
            pipeline.append(sort_stage)

        if page and per_page:
            skip_stage = {'$skip': (page - 1) * per_page}
            pipeline.append(skip_stage)
        # Add $limit stage based on limit_value
        if per_page:
            limit_stage = {'$limit': per_page}
            pipeline.append(limit_stage)
        print(pipeline)
        documents = self.collection.aggregate(pipeline)
        return [self.model_class(**{key: doc[key] for key in doc if key not in exclude_keys}) for doc in documents]

    def aggregate_raw(self, pipeline):
        documents = self.collection.aggregate(pipeline)
        return documents

    def aggregate_count(self, pipeline, query=None):
        if query:
            pipeline[0]["$lookup"]["pipeline"].append({"$match": query})

        count_stage = {'$count': 'documentCount'}
        pipeline.append(count_stage)
        print(pipeline)
        document = list(self.collection.aggregate(pipeline))
        if document:
            document_count = document[0].get('documentCount', 0)
            return document_count
        else:
            return 0

    def count_documents(self, query):
        return self.collection.count_documents(query)
