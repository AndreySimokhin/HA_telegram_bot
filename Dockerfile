FROM python:3.11-slim-bullseye

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN \
    set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    && apt-get purge -y --auto-remove

# Python 3 Telegram FTP bot serves the current working dir
# So let's set it to our add-on persistent data directory.
WORKDIR /home

# Install requirements for add-on
COPY requirements.txt /home/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy data for add-on
COPY /Telegram_FTP_Bot/ /home/Telegram_FTP_Bot/
COPY config.yaml /home/

CMD [ "python3", "Telegram_FTP_Bot" ]
