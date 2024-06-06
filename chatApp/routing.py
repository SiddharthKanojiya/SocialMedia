from django.urls import path,re_path
from chatApp.consumers import MychatApp

websocket_urlpatterns =[

    path('ws/wsc/',MychatApp.as_asgi()),
    re_path(r'ws/wsc/group/(?P<room_name>\w+)/$', MychatApp.as_asgi()),
]