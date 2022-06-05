from django.contrib import admin
from django.urls import path
from .views import RegisterView, LoginApiView, LogoutApiView, ChangePasswordApiView


# path("register/", UserView.as_view()),
# path("change_password/", ChangePasswordView.as_view()),
# path("logout/", LogoutApiView.as_view()),
urlpatterns = [
    # path("login/", loginApi),
    # path("get_user/", get_User),
    path("register/", RegisterView.as_view()),
    path("login/", LoginApiView.as_view()),
    path("change_password/<int:pk>", ChangePasswordApiView.as_view()),
    path("logout/", LogoutApiView.as_view()),
]
