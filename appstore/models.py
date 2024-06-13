from bson import ObjectId
from django.db import models


class HbAppStoreMaster(models.Model):
    _id = models.CharField(max_length=24, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    description = models.TextField()
    rating = models.CharField(max_length=10)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())  # Replace with your ID generation logic
        super(HbAppStoreMaster, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hb_app_store_master'

    def __str__(self):
        return self.name


class HbAppStoreEntityMapping(models.Model):
    _id = models.CharField(max_length=24, primary_key=True, editable=False)
    entityCode = models.CharField(max_length=255)
    appStoreCode = models.CharField(max_length=10)
    apiKey = models.CharField(max_length=255)
    apiSecret = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())  # Replace with your ID generation logic
        super(HbAppStoreEntityMapping, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hb_app_store_entity_mapping'

    def __str__(self):
        return self.entityCode + self.appStoreCode


class ApiLogging(models.Model):
    _id = models.CharField(max_length=24, primary_key=True, editable=False)
    entityCode = models.CharField(max_length=255)
    appStoreCode = models.CharField(max_length=10)
    apiEndpoint = models.CharField(max_length=255)
    payload = models.TextField()
    response = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())  # Replace with your ID generation logic
        super(ApiLogging, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hb_api_logging'

    def __str__(self):
        return self.entityCode + self.appStoreCode
