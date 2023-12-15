from django.urls import path
from .views import sign_up, profile, sign_in, user_logout

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("sign-up/", sign_up, name="sign_up"),
    path("sign-in/", sign_in, name="sign_in"),
    path("logout/", user_logout, name="logout"),
]
