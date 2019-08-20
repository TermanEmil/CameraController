from django.urls import path

from proj_logging.views.logs import LogsList, LogsDelete, LogsDeleteAll

urlpatterns = [
    path('', LogsList.as_view(), name='all_logs'),
    path('delete/<int:pk>', LogsDelete.as_view(), name='delete'),
    path('delete/all', LogsDeleteAll.as_view(), name='delete/all'),
]