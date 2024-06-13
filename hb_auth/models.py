from bson import ObjectId
from django.db import models

# Create your models here.

from django.db import models
import uuid


class HbApplications(models.Model):
    _id = models.CharField(max_length=24, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())  # Replace with your ID generation logic
        super(HbApplications, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hb_applications'

    def __str__(self):
        return self.name


class ClientDetail(models.Model):
    _id = models.CharField(max_length=24, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    apiKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reqCount = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())  # Replace with your ID generation logic
        super(ClientDetail, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hb_client_details'

    def __str__(self):
        return self.name
