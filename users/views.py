from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.views.generic import CreateView
from orders.models import OrderModel, OrderItemModel
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# Create your views here.


@login_required
def profile(request):
    orders = OrderModel.objects.filter(user=request.user)
    print(orders)
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
    print(order_list)
    isOrderExists = len(order_list)
    return render(request, "profile.html", {"form": form, "type": "User Profile", "orders": order_list, "isOrderExists": isOrderExists, "total_price": total_price})


class UserSignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy("sign_in")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Signed up successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Invalid user credentials")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Sign up"
        return context


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


@login_required
def change_password(request):
    if (request.method == "POST"):
        form = SetPasswordForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success("Password changed successfully")
            return redirect("profile")

    else:
        form = SetPasswordForm(user=request.user)

    return render(request, "change_password.html", {"form": form, "type": "Change Password"})


def user_logout(request):
    logout(request)
    return redirect("home")


class UserLogoutView(LogoutView):
    template_name = "logout.html"

    def get_success_url(self):
        return reverse_lazy("home")
