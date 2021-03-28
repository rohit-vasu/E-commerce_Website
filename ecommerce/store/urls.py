from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('OurTeam/', views.OurTeam, name="OurTeam"),

    path('update_item/', views.updateItem, name="update_item"),

    path('register/', views.registerPage , name="register"),
    path('login/', views.loginPage , name="login"),
]


