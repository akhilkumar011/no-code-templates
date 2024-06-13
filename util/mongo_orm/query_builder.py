class QueryBuilder:
    def __init__(self, repository):
        self.repository = repository
        self.query = {}

    def filter(self, field, value):
        self.query[field] = value
        return self

    def execute(self):
        return self.repository.find(self.query)
