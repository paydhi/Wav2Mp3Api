from django.urls import path
from records.views import UploadRecordView#, DownloadRecordView

urlpatterns = [
    path('upload_record/', UploadRecordView.as_view(), name='upload_record'),
    # path('download/', DownloadRecordView.as_view(), name='download_record'),
]