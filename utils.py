import logging
import traceback

import aiohttp

from config import Config
import urllib.request
logging.getLogger().setLevel(logging.INFO)

async def ping_server():
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(Config.REPLIT) as resp:
                logging.info(f"Pinged server with response: {resp.status}")
    except TimeoutError:
        logging.warning("Couldn't connect to the site URL..!")
    except Exception:
        traceback.print_exc()

async def getResponse(url, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, raise_for_status=True) as response:
            data = await response.json() # get json response data from url
            return data

# for always run on replit
if Config.REPLIT:
    from threading import Thread

    from flask import Flask, jsonify
    app = Flask('')
    @app.route('/')
    def main():
        res = {
            "status":"running",
            "hosted":"replit.com",
        }
        return jsonify(res)

    def run():
        app.run(host="0.0.0.0", port=8000)
    
    async def keep_alive():
        server = Thread(target=run)
        server.start()

def get_text(title, date, media_type, copyright, url=None):
    descriptipn_url = "https://apod.nasa.gov/apod/astropix.html"
    template = f"Title: {title} - {date}\n\nDescription\n{descriptipn_url}\n\n© {copyright}"
    if media_type == 'video':
        template += f"\n\n{url}"
    return template

def get_picture(url, full_path):
    urllib.request.urlretrieve(url, full_path)