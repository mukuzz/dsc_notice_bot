
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Notice
from .update import update_db
from django.core import serializers

def getNewCount(request, old_key):
	latest_key = 0
	new_objects = Notice.objects.filter(key__gt=old_key)
	data = {'new_count':len(new_objects)}
	return JsonResponse(data)


def get_notices(request, latest_key):
	required_objects = Notice.objects.filter(key__gt=latest_key)
	data = serializers.serialize('json', required_objects, fields=('title','key','content'))
	return HttpResponse(data)