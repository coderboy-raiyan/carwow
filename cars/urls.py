from django.urls import path
from . import views

urlpatterns = [
    path("details/<int:id>", views.CarDetailsView.as_view(), name="car_details"),
    path("buy/<int:id>", views.buy_now, name="buy_car")
]
