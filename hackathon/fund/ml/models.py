from django.db import models

# Create your models here.
class Problem(models.Model):
    file_store=models.FileField(upload_to='media/')