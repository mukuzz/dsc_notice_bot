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

# Usage
Start a local server on port 8888:

    ./manage.py runserver 0:8888

In a new terminal start a Celery Beat Scheduler

    celery -A DSC_Backendeat -l info

In another new terminal start a celery worker

    celery -A DSC_Backend worker -l info

The server will now start scrapping the [College Website](http://dsc.du.ac.in/AllNewsDetails.aspx) for updates and send message to the specified Telegram Channel