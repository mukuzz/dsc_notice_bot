# Dyal Singh College Bot
This is the backend for the Dyal Sing College Bot.

# Features
* Send latest notices (scrapped from [College Website](http://dsc.du.ac.in/AllNewsDetails.aspx)) to [Telegram Channel](https://tlgrm.eu/channels)

# Installation
Clone the repository:

    git clone https://github.com/mukuz97/DSC-Backend.git DSC_Backend
    cd DSC_Backend/

Install non python requirements:

    sudo apt install redis-server

Create a virtual environment and install python requirements

    virtualenv --python=python3 venv # note that python3 is required
    source venv/bin/activate
    pip install -r requirements.txt

# Configuration
Create the configuration file at `/opt/DSC_Backend/config.ini` and add these configurations to the file:

    [secrets]
    SECRET_KEY: <LONG_UNICODE_STRING>

    [telegram]
    BOT_TOKEN: <TELEGRAM_BOT_TOKEN>
    TARGET_CHANNEL: <TELEGRAM_CHANNEL_ID>

TELEGRAM_CHANNEL_ID should begin with `@`

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

## Developmet

In development we will need to run the redis-server as a daemon. Open this file with your preferred text editor:

    sudo nano /etc/redis/redis.conf

Inside the file, find the `daemonise` directive. We need this directive to have value `yes`

    . . .

    # By default Redis does not run as a daemon. Use 'yes' if you need it.
    # Note that Redis will write a pid file in /var/run/redis.pid when daemonized.
    daemonize yes

    . . .

Now restart the Redis service to reflect the changes we made to the configuration file:

    sudo systemctl restart redis.service

# Production Deployment

## Install requirements

    pip install gunicorn
    sudo apt install supervisor

## Configuration

Open this file with your preferred text editor:

    sudo nano /etc/redis/redis.conf

Inside the file, find the `daemonise` directive. We need this directive to have value `no` as we want to supervise our redis server with superviserd:

    . . .

    # By default Redis does not run as a daemon. Use 'yes' if you need it.
    # Note that Redis will write a pid file in /var/run/redis.pid when daemonized.
    daemonize no

    . . .

Now stop the Redis service

    sudo systemctl stop redis.service

Edit `/etc/supervisor/conf.d/DSC_Backend.conf`

    [group:DSC_Backend]
    programs=gunicorn,redis,celery,celery-beat

    [program:gunicorn]
    command=/home/mukul/DjangoProjects/pyhton3.6_env/bin/gunicorn --name DSC_Backend --workers 12 --bind 127.0.0.1:8888 --log-level=INFO DSC_Backend.wsgi:application
    directory=/home/mukul/DjangoProjects/DSC_Backend/
    autostart=true
    autorestart=true

    [program:redis]
    command=redis-server

    [program:celery]
    command=/home/mukul/DjangoProjects/pyhton3.6_env/bin/celery -A DSC_Backend worker -l info
    directory=/home/mukul/DjangoProjects/DSC_Backend/
    autostart=true
    autorestart=true

    [program:celery-beat]
    command=/home/mukul/DjangoProjects/pyhton3.6_env/bin/celery -A DSC_Backend beat -l info
    directory=/home/mukul/DjangoProjects/DSC_Backend/
    autostart=true
    autorestart=true

Reload the configuration:

    sudo supervisorctl update

Restart all DSC_Backend services:

    sudo supervisorctl restart videofront: