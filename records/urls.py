from django.urls import path
from .views import report_view,report
urlpatterns = [
    path('', report_view,name="report_view"),
    path('full_report', report,name="full_report"),
]