from celery import task
from .models import SentNotice
from Notices.models import Notice
import requests
from django.conf import settings
from celery.utils.log import get_task_logger
import redis

target = settings.TELEGRAM_TARGET_CHANNEL
token = settings.TELEGRAM_BOT_TOKEN

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes
REDIS_CLIENT = redis.Redis()
key = "send_notices_to_channel"

logger = get_task_logger(__name__)

@task
def sendNewNoticesToChannel(new_notices):
	# new_notices argument takes the input from the earlier
	# task in chain of celery tasks that is update_db

	lock = REDIS_CLIENT.lock(key, timeout=LOCK_EXPIRE)
	try:
		have_lock = lock.acquire(blocking=False)
		if have_lock:
			# Run the task as no other instance running

			if len(new_notices) > 0:
				try:
					last_sent_notice = SentNotice.objects.order_by('-key')[0:1].get()
					last_sent_notice_key = last_sent_notice.key
				except SentNotice.DoesNotExist:
					last_sent_notice_key = 0
				# Send the last 10 notices
				new_notices = Notice.objects.filter(key__gt=last_sent_notice_key).order_by('key')[:10]

				response_codes = []
				for notice in new_notices:
					chat_text = notice.content  
					response = requests.get(
						f'https://api.telegram.org/bot{token}/sendMessage',
						params = {
							'chat_id': target,
							'text': chat_text,
							'parse_mode': 'html',
							'disable_web_page_preview': 'true'
						}
					)
					response_codes.append(response.status_code)
					if response.status_code == 200:
						sent_notice = SentNotice(key=notice.key, notice=notice)
						sent_notice.save()
				return response_codes
		else:
			logger.info("One instance of task alreday running")
	finally:
		if have_lock:
			lock.release()

