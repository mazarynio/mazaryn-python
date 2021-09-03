from django.urls import path
from .views import all_messages, MessageWithOneFriendView,SendMessageToOneFriendView

app_name = "communications"

urlpatterns = [
    path('getallmessages', all_messages, name="all-messages"),
    path('getfriendmessages',MessageWithOneFriendView.as_view(), name="messages-with-one-friend"),
    path('sendmessagetofriend',SendMessageToOneFriendView.as_view(), name="send-message-to-friend"),
]
