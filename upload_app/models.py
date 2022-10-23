from django.db import models

# Create your models here.
class UploadFile(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    body = models.TextField()

    # Ko có cái này thì table tạo ra theo appname_classmodel
    # class Meta:
    #     managed = True
    #     db_table = 'uploadapp_uploadfile'