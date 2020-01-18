from django.core.management.base import BaseCommand, CommandError
from Notices.tasks import update_db
from TelegramBot.tasks import sendNewNoticesToChannel
from Notices.models import Notice
from TelegramBot.models import SentNotice

import requests
import re
import bs4
import hashlib

SOURCE_URL = 'http://dsc.du.ac.in/'
NOTICES_URL = SOURCE_URL


class Command(BaseCommand):

    def handle(self, *args, **options):
        request = requests.get(NOTICES_URL)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        data = soup.find_all('marquee')
        notices = []
        for d in data:
            for notice in d.find_all('a'):
                notices.append(notice)
        new_notices = []
        for notice in notices:
            text = notice.text.strip()
            url =  notice.attrs['href']
            if url[:4] != 'http':
                url =  SOURCE_URL + notice.attrs['href'][3:]
            content = f'\n\n<a href="{url}">{url}</a>'
            key = hashlib.md5(text.encode('utf-8')).hexdigest()
            # Get the notice with old key
            try:
                curr_notice = Notice.objects.get(key=key)
                curr_sent_notice = SentNotice.objects.get(key=key)
                new_key = hashlib.md5((text+url).encode('utf-8')).hexdigest()
                curr_notice.key = new_key
                curr_notice.save()
                curr_sent_notice.key = new_key
                curr_sent_notice.save()
            except Exception:
                print('Already fixed')