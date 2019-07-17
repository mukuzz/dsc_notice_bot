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

Open this file with your preferred text editor:

    sudo nano /etc/redis/redis.conf

Inside the file, find the `supervised` directive. This directive allows us to declare an init system to manage Redis as a service, providing us with more control over its operation. The supervised directive is set to `no` by default. Since we are running Ubuntu, which uses the systemd init system, change this to `systemd`:

    . . .

    # If you run Redis from upstart or systemd, Redis can interact with your
    # supervision tree. Options:
    #   supervised no      - no supervision interaction
    #   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
    #   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
    #   supervised auto    - detect upstart or systemd method based on
    #                        UPSTART_JOB or NOTIFY_SOCKET environment variables
    # Note: these supervision methods only signal "process is ready."
    #       They do not enable continuous liveness pings back to your supervisor.
    supervised systemd

    . . .

Now restart the Redis service to reflect the changes we made to the configuration file:

    sudo systemctl restart redis.service

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

The server will now start scrapping the [College Website](http://dsc.du.ac.in/AllNewsDetails.aspx) for updates and send message to the specified Telegram Channel