from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:user>/create", views.create, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("watchlist", views.watchlistView, name="watchlistView"),
    path("my-profile", views.profile, name="profile"),
    path("categories", views.categoriesDisplay, name="categories"),
    path("category/<str:cat>", views.specificcat, name="cat")
]
