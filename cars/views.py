from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import OrderModel, OrderItemModel
# Create your views here.


def car_details(request, id):
    car = models.CarModel.objects.get(pk=id)
    return render(request, "car_details.html", {"car": car})


@login_required
def buy_now(request, id):
    car = models.CarModel.objects.get(pk=id)
    if (car.quantity > 0):
        car.quantity = car.quantity - 1
        # set order
        order = OrderModel()
        order.user = request.user
        order.total_amount = car.price

        car.save()
        order.save()
        # set item
        order_item = OrderItemModel()
        order_item.order = order
        order_item.car = car
        order_item.quantity = 1

        order_item.save()

        messages.success(request, "Order placed successfully")
    else:
        messages.warning(request, "Sorry order is out of stock !!")

    dynamic_url = reverse("car_details", args=[car.id])
    return redirect(dynamic_url)
