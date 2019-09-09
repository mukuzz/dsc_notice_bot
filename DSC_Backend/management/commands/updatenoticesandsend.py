from django.core.management.base import BaseCommand, CommandError
from Notices.tasks import update_db
from TelegramBot.tasks import sendNewNoticesToChannel


class Command(BaseCommand):
    help = 'Update Notices from source and send if new ones available to telegram channel'

    def handle(self, *args, **options):
        new_keys = update_db()
        sendNewNoticesToChannel(new_keys)
