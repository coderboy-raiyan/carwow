from django.urls import path
from .views import sign_up, profile, sign_in, user_logout, change_password, UserLogoutView, UserSignUpView


urlpatterns = [
    path("profile/", profile, name="profile"),
    path("sign-up/", UserSignUpView.as_view(), name="sign_up"),
    path("sign-in/", sign_in, name="sign_in"),
    path("change-password/", change_password, name="change_password"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
