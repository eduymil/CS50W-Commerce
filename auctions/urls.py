from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<str:user>/<int:title>", views.indi, name="indi"),
    path("comment", views.comment, name="comment"),
    path("<str:user>/watchlist",views.watchlist, name="watchlist"),
    path("<int:title>/bid",views.bid, name="bid"),
    path("<int:title>/close",views.close, name="close"),
    path("inactive",views.inactive, name="inactive"),
    path("category/<str:cat>",views.category, name="category")
]