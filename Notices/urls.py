
from django.urls import path
from . import views

urlpatterns = [
	# Returns the latest key
    path('check_new/', views.check_new, name='CheckNew'),
    # Returns notices after the mentioned key
    path('get/<int:latest_key>/', views.get_notices, name='GetNotices'),
    # Update Notice Database
    path('update/', views.update_notices, name='UpdateNotices')
]