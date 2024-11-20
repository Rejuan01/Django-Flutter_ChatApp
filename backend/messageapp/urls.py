
from django.urls import path
from .views import MyInboxView, GetMessagesView, SendMessageView, SearchUserView

urlpatterns = [
    path('inbox/<user_id>/', MyInboxView.as_view(), name = 'inbox'),
    path('get/<sender_id>/<receiver_id>/', GetMessagesView.as_view(), name = 'getMessages'),
    path('send/', SendMessageView.as_view(), name = 'sendMessage'),
    path('search/<username>', SearchUserView.as_view(), name = 'searchUser')
]
