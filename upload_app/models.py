from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class UploadFile(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/')
    # body = models.TextField()
    body = RichTextField()

    # Ko có cái này thì table tạo ra theo appname_classmodel
    # class Meta:
    #     managed = True
    #     db_table = 'uploadapp_uploadfile'