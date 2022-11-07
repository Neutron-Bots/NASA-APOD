import asyncio
import logging
import os
import time

import schedule
import tweepy

from config import Config
from utils import get_picture, get_text, getResponse, ping_server

logging.getLogger().setLevel(logging.INFO)

# Credentials
api_key = Config.API_KEY
api_secret = Config.API_SECRET
bearer_token = fr"{Config.BEARER_TOKEN}"
access_token = Config.ACCESS_TOKEN
access_token_secret = Config.ACCESS_TOKEN_SECRET

# Gainaing access and connecting to Twitter API using Credentials
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

# Creating API instance. This is so we still have access to Twitter API V1 features
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

        
async def tweet(tweepy: tweepy.Client):
    data = await getResponse(Config.url)
    copyright = data.get('copyright', None)
    date = data.get('date', None)
    media_type = data.get('media_type', None)
    title = data.get('title', None)
    url = data.get('hdurl') if 'hdurl' in data else data.get('url')

    text = get_text(title, date, media_type, copyright, url)

    media_id = None

    if media_type == 'image' and '.gif' not in url:
        path = 'image.png'
        get_picture(url, path)
        upload_media = api.media_upload(filename=path)
        media_id = upload_media.media_id_string
        os.remove(path)

    tweepy.create_tweet(text=text, media_ids=[media_id] if media_id else None)


def main():
    try:
        asyncio.run(tweet(client))
    except Exception as e:
        logging.error(e)


def ping_server_main():
    asyncio.run(ping_server())

schedule.every(1).day.do(main)

if Config.REPLIT:
    from utils import keep_alive
    asyncio.run(keep_alive())
    schedule.every(4).minutes.do(ping_server_main)

if __name__ ==  "__main__":
    logging.info("Bot starting...")

    # main()
    while True:
        schedule.run_pending()
        time.sleep(1)