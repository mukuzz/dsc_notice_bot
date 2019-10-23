# Dyal Singh College Bot
This is the backend for the Dyal Sing College Bot.

# Features
* Send latest notices (scrapped from [College Website](http://dsc.du.ac.in/)) to [Telegram Channel](https://tlgrm.eu/channels)

# Installation
Clone the repository:

    git clone https://github.com/mukuz97/DSC-Backend.git DSC_Backend
    cd DSC_Backend/

Create a virtual environment and install python requirements

    virtualenv --python=python3 venv # note that python3 is required
    source venv/bin/activate
    pip install -r requirements.txt

# Configuration
Create the following environment variables:

    SECRET_KEY:
    DATABASE_PASSWORD:
    DATABASE_URL:
    TELEGRAM_BOT_TOKEN:
    TELEGRAM_TARGET_CHANNEL:

TELEGRAM_CHANNEL_ID should begin with `@`


Make Django migrations

    ./manage.py migrate

# Usage
Start a local server on port 8888:

    ./manage.py runserver 0:8888

To update the database run:

    ./manage.py updatenoticesandsend

The server will scrape the source for updates and send message to the specified Telegram Channel