from django.urls import path
from .views import RegisterView, LoginView, CheckTokenView, ProfileDetail

urlpatterns = [
    path('signup/', RegisterView.as_view(), name = 'signup'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('checktoken/', CheckTokenView.as_view(), name = 'check_token'),
    path('profile/<int:pk>', ProfileDetail.as_view(), name = 'profile')
]

