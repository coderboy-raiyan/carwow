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
    if (car.quantity > 0):
        car.quantity = car.quantity - 1

        is_any_order_exists = OrderItemModel.objects.all().exists()
        if is_any_order_exists:
            find_the_car = OrderItemModel.objects.filter(car=car).exists()

            if find_the_car:
                getCar = OrderItemModel.objects.get(car=car)
                getCar.quantity = getCar.quantity+1
                getCar.save()
                messages.success(
                    request, f"Successfully added one more of this {car.car_name} to your order.")
                car.save()
            else:
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
