from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from orders.models import OrderModel, OrderItemModel
# Create your views here.


@login_required
def profile(request):
    orders = OrderModel.objects.filter(user=request.user)
    order_list = []
    for order in orders:
        ordered_item = OrderItemModel.objects.get(order=order)
        order_list.append(ordered_item)

    total_price = 0
    for order in order_list:
        total_price += order.quantity * order.car.price

    if (request.method == "POST"):
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("profile")
    else:
        form = UpdateUserForm(instance=request.user)

    return render(request, "profile.html", {"form": form, "type": "User Profile", "orders": order_list, "total_price": total_price})


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("home")

    if (request.method == "POST"):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created Successfully")
            return redirect("sign_in")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form, 'type': 'Sign up'})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("home")

    if (request.method == "POST"):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("profile")
            else:
                messages.warning(request, "User not found")
                return redirect("register")
    else:
        form = AuthenticationForm()

    return render(request, "sign_in.html", {"form": form, "type": "Sign in"})


def user_logout(request):
    logout(request)
    return redirect("home")
