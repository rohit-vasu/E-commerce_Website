from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('OurTeam/', views.OurTeam, name="OurTeam"),

    path('update_item/', views.updateItem, name="update_item"),

    path('register/', views.registerPage , name="register"),
    path('login/', views.loginPage , name="login"),

    #password reset urls
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='store/password_reset.html'),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_sent.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_form.html'),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='store/password_reset_done.html'),name="password_reset_complete"),
]


