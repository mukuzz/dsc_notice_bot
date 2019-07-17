from celery import Celery
from .models import BotUser
from Notices.models import Notice
from Notices.tasks import update_db
import requests
from django.conf import settings

app = Celery()

target = settings.TELEGRAM_TARGET_CHANNEL
token = settings.TELEGRAM_BOT_TOKEN

@app.task
def sendNewNoticesToChannel(new_notice_count):
  # an argument is required for this function
  # to work properly when this task is chained
  # in celery *Celery Shit*

  if len(new_notice_count) > 0:
    min_key = min(new_notice_count)
    new_notices = Notice.objects.filter(key__gte=min_key)

    response_codes = []
    for notice in reversed(new_notices):
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
    return response_codes

