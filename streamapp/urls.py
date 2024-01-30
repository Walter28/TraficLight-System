from django.urls import path
from . import views
# from .views import nbRoad

urlpatterns = [
    path('', views.index, name='index'),
    path('setting', views.setting, name='setting'),
    # path('video_feed', views.video_feed,  name='video_feed'),
    path('video_feed_road1', views.video_feed_road1,  name='video_feed_road1'),
    path('video_feed_road2', views.video_feed_road2,  name='video_feed_road2'),
    path('video_feed_road3', views.video_feed_road3,  name='video_feed_road3'),
    path('video_feed_road4', views.video_feed_road4,  name='video_feed_road4'),
    path('ajax/change_road', views.change_road, name='change_road'),
    path('ajax/page_load', views.page_load, name='page_load'),
    path('ajax/road_set_camera', views.road_set_camera, name='road_set_camera'),
    # path('ajax/frame_size', views.frame_size, name='frame_size'),
    path('ajax/road_take_photo', views.road_take_photo, name='road_take_photo'),
    path('ajax/receive_coord', views.receive_coord, name='receive_coord'),
]
