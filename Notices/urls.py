
from django.urls import path
from . import views

urlpatterns = [
	# Returns the count of new notices after the given key
    path('get_new_count/<int:old_key>/', views.getNewCount, name='getNewCount'),
    # Returns notices after the mentioned key
    path('get/<int:latest_key>/', views.get_notices, name='GetNotices'),
]