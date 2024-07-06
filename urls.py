from django.urls import path
from .views import PassChangeView, SendMoneyView

urlpatterns = [
    path("pass_change/", PassChangeView.as_view(), name="pass_change"),
    path("sendmoney/", SendMoneyView.as_view(), name="sendmoney"),
]
