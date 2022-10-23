from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'upload'

urlpatterns = [
    # Using template
    path('', views.UploadImage.as_view(), name='upload_template'),
    path('<int:pk>/', views.UploadImageDisplay.as_view(), name='view_upload_template_page'),

    # Using model form
    path('uploadmodelform/', views.uploadFile, name = 'upload_modelform'),
    path('uploadmodelform/getFile/', views.getFile, name = 'view_upload_modelform_page'),
    # path('getFile/<int:pk>/', views.getFile, name = 'getfile'),

    # Using form custom
    path('custom/', views.uploadFileCustom, name = 'upload_customform'),
    path('custom/getFileCustom/', views.getFileCustom, name = 'upload_customform_page'),
    path('custom/uploadcustom-image/<int:pk>/', views.uploadFileCustomForm_view, name = 'view_upload_customform_page'),

]