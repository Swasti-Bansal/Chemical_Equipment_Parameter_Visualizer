from django.urls import path
from .views import upload_csv
from .views import history_api
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import report_pdf

urlpatterns = [
    path("upload/", upload_csv),
    path("history/", history_api),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("report/", report_pdf),
]

