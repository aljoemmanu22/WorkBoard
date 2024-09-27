from django.urls import re_path
from boards.consumers import TaskBoardConsumer

websocket_urlpatterns = [
    re_path(r'ws/boards/(?P<board_id>\w+)/$', TaskBoardConsumer.as_asgi()),
]
