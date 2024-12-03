from django.urls import path
from .views import *

urlpatterns = [
    # Signup view
    path("signup/", UserSignupForm.as_view(), name="signup"),
    path('',LoginView.as_view(),name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # Custom password reset views
    path("password_reset/", CustomPasswordResetView.as_view(), name="custom_password_reset"),
    path("password_reset_done/", CustomPasswordResetDoneView.as_view(), name="custom_password_reset_done"),
    path("password_reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="custom_password_reset_confirm"),
    path("password_reset_complete/", CustomPasswordResetCompleteView.as_view(), name="custom_password_reset_complete"),
]
