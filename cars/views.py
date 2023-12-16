from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import OrderModel, OrderItemModel
from django.views.generic import CreateView, DetailView
from django.utils.decorators import method_decorator
from users.models import CarModel
from users.forms import CommentForm
# Create your views here.


class CarDetailsView(DetailView):
    model = CarModel
    template_name = "car_details.html"
    pk_url_kwarg = "id"

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        car = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.email = self.request.user.email
            new_comment.car = car
            new_comment.save()
            messages.success(request, "Thanks for your comment")
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        comments = car.comments.order_by('-createdAt')
        comment_form = CommentForm()
        context['car'] = car
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context


@login_required
def buy_now(request, id):
    car = models.CarModel.objects.get(pk=id)
    dynamic_url = reverse("car_details", args=[car.id])

    if (car.quantity <= 0):
        messages.warning(request, "Sorry order is out of stock !!")
        return redirect(dynamic_url)

    # set item
    is_any_order_exists = OrderModel.objects.all().exists()
    is_any_order_item_exists = OrderItemModel.objects.all().exists()

    if is_any_order_exists and is_any_order_item_exists:
        find_item = OrderItemModel.objects.filter(car=car)
        is_new_car = True
        for userCar in find_item:
            if userCar.order.user == request.user:
                is_new_car = False
                userCar.quantity = userCar.quantity+1
                userCar.save()
                car.quantity = car.quantity - 1
                messages.success(
                    request, f"Successfully added one more of this {car.car_name} to your order.")

        if is_new_car:
            order = OrderModel()
            order.user = request.user
            order.total_amount = car.price
            order.save()
            order_item = OrderItemModel()
            order_item.order = order
            order_item.car = car
            order_item.quantity = 1
            order_item.save()
            car.quantity = car.quantity - 1
            messages.success(request, "Order placed successfully")
    else:
        order = OrderModel()
        order.user = request.user
        order.total_amount = car.price
        order.save()
        order_item = OrderItemModel()
        order_item.order = order
        order_item.car = car
        order_item.quantity = 1
        order_item.save()
        car.quantity = car.quantity - 1
        messages.success(request, "Order placed successfully")
    car.save()

    return redirect(dynamic_url)
