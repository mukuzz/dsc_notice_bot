# Dyal Singh College Bot
This is the backend for the Dyal Sing College Bot.

# Features
* Send latest notices (scrapped from [College Website](http://dsc.du.ac.in/AllNewsDetails.aspx)) to [Telegram Channel](https://tlgrm.eu/channels)

# Installation
Clone the repository:

    git clone https://github.com/mukuz97/DSC-Backend.git DSC_Backend
    cd DSC_Backend/

Install non python requirements:

    sudo apt install redis-server build-essential

Create a virtual environment and install python requirements

    virtualenv --python=python3 venv # note that python3 is required
    source venv/bin/activate
    pip install -r requirements.txt

# Configuration
Create the configuration file at `/opt/DSC_Backend/config.ini` and add these configurations to the file:

    [secrets]
    DJANGO_SECRET_KEY: <LONG_UNICODE_STRING>
    POSTGRESQL_PASSWORD: <LONG_UNICODE_STRING>

    [telegram]
    BOT_TOKEN: <TELEGRAM_BOT_TOKEN>
    TARGET_CHANNEL: <TELEGRAM_CHANNEL_ID>

TELEGRAM_CHANNEL_ID should begin with `@`

Configure the postgresql server as shown
[here](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)

Make Django migrations

    ./manage.py migrate

# Usage
Start a local server on port 8888:

    ./manage.py runserver 0:8888

In a new terminal start a Celery Beat Scheduler

    celery -A DSC_Backend beat -l info

In another new terminal start a celery worker

    celery -A DSC_Backend worker -l info

Also make sure that the redis server is running

The server will now start scrapping the [College Website](http://dsc.du.ac.in/AllNewsDetails.aspx) for updates and send message to the specified Telegram Channel

# Production Deployment

## Directory Structure

    /opt/DSC_Backend/
        DSC_Backend
        Notices
        TelegramBot
        celerybeat-schedule
        manage.py
        venv/bin/
            celery
            gunicorn

## Install requirements

    pip install gunicorn
    sudo apt install supervisor

## Configuration

Edit `/etc/supervisor/conf.d/DSC_Backend.conf`

    [group:DSC_Backend]
    programs=gunicorn,celery,celery-beat

    [program:gunicorn]
    command=/opt/DSC_Backend/venv/bin/gunicorn --name DSC_Backend --workers 1 --bind 0:8000 --log-level=INFO DSC_Backend.wsgi:application
    directory=/opt/DSC_Backend/
    autostart=true
    autorestart=true
    user=mukul

    [program:celery]
    command=/opt/DSC_Backend/venv/bin/celery -A DSC_Backend worker -l info
    directory=/opt/DSC_Backend/
    autostart=true
    autorestart=true
    user=mukul

    [program:celery-beat]
    command=/opt/DSC_Backend/venv/bin/celery -A DSC_Backend beat -l info
    directory=/opt/DSC_Backend/
    autostart=true
    autorestart=true
    user=mukul

Reload the configuration:

    sudo supervisorctl update

Restart all DSC_Backend services:

    sudo supervisorctl restart videofront: