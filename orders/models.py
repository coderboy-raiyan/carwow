from django.db import models
from django.contrib.auth.models import User
from cars.models import CarModel
# Create your models here.


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.car.car_name
