from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.my_notifications, name="notification-list"),
    path("unread-count/", views.unread_count, name="unread-count"),
    path("<uuid:notification_id>/read/", views.mark_read, name="mark-read"),
    path("read-all/", views.mark_all_read, name="mark-all-read"),
    path("activity/", views.activity_feed, name="activity-feed"),
]
