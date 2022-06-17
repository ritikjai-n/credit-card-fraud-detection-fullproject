from datetime import datetime
from django.db import models

# Create your models here.
class updation(models.Model):
    sno = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    uploading = models.FileField(upload_to ='upload/')
