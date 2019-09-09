from .models import SentNotice
from Notices.models import Notice
import requests
from django.conf import settings

target = settings.TELEGRAM_TARGET_CHANNEL
token = settings.TELEGRAM_BOT_TOKEN


def sendNewNoticesToChannel(new_notices):
	# new_notices argument takes the input from the earlier
	# task in chain of tasks that is update_db

	try:
		sent_notices = SentNotice.objects.all()
		sent_notice_keys = [notice.key for notice in sent_notices]
	except SentNotice.DoesNotExist:
		sent_notice_keys = []
	# Select 10 of the new notices
	new_notices = [notice for notice in Notice.objects.all() if notice.key not in sent_notice_keys]
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
