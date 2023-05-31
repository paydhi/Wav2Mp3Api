from django.urls import path
from records.views import UploadRecordView

urlpatterns = [
    path('upload_record/', UploadRecordView.as_view(), name='upload_record'),
]
