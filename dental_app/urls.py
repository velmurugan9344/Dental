from django.urls import path
from . import views
from .views import register_view, login_view, logout_view
from .views import forgot_password
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('appointment', views.appointment, name='appointment'),
    path('contact', views.contact, name='contact'),
    path('testimonial', views.testimonial, name='testimonial'),
    path('team', views.team, name='team'),
    path('price', views.price, name='price'),
    path('service', views.service, name='service'),

    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),

    path('make-appointment/', views.make_appointment, name='make_appointment'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('contact/', views.contact_view, name='contact'),

    path('subscribe/', views.subscribe, name='subscribe'),
    path('search-doctors/', views.search_doctors, name='search_doctors'),
    path('search-not-found/', views.search_not_found, name='search_not_found'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    #Forgot password
    # Password Reset Request (Forgot Password)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
        name="password_reset",
    ),

    # Password Reset Done (Email Sent)
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_done",
    ),

    # Password Reset Confirm (User Clicks Reset Link)
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),

    # Password Reset Complete (Successful Reset)
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),

]