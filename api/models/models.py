from bson import ObjectId
from django.db import models


# Create your models here.


class HbAppEntity(models.Model):
    _id = models.CharField(max_length=24, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    entityCode = models.UUIDField()
    description = models.TextField()
    applicationCode = models.CharField(max_length=10)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())  # Replace with your ID generation logic
        super(HbAppEntity, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hb_app_entities'

    def __str__(self):
        return self.name
