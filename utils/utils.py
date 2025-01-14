import os

import nextcord
from nextcord.ext import tasks
import datetime
import json

from logic.advanced_forecast import generate_graphs_image
from logic.forecast_image import generate_forecast_image
from ui import message_templates
from utils.bot_object_holder import BotObjectHolder

OUR_SERVER_ID = 913375693864308797


def get_client_token():
    return os.getenv('CLIENT_TOKEN')


def get_guild_id_by_channel_id(channel_id):
    with open("data/config.json") as file:
        data = json.load(file)

    for channel in data['BroadcastChannels']:
        if channel['ChannelId'] == channel_id:
            return channel['ServerId']

    return ''


def load_extensions(client):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'    {filename[:-3]}')


def generate_images():
    generate_forecast_image()
    generate_graphs_image()


def get_channels():
    with open("data/config.json") as file:
        data = json.load(file)

    return data["BroadcastChannels"]


# sends stats to the channels defined i the file data/config.json
# to add a channel to the config run 'channel set' command on the channel
async def broadcast_stats():
    channel_list = get_channels()
    client = BotObjectHolder.get_bot()
    print(client)

    for el in channel_list:
        channel_id = el["ChannelId"]
        channel = client.get_channel(channel_id)
        print(channel)

        forecast_image = nextcord.File('./assets/generated_images/image.png')

        if get_guild_id_by_channel_id(channel_id) == str(OUR_SERVER_ID):
            embed = await message_templates.daily_stats_embed(forecast_image.filename, our_server=True)
            await channel.send(embed=embed,
                               files=[forecast_image])
        else:
            embed = await message_templates.daily_stats_embed(forecast_image.filename)
            await channel.send(embed=embed,
                               files=[forecast_image])


@tasks.loop(minutes=30)
async def send_stats():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    if 4 <= hour < 5:
        if 15 <= minute < 45:
            print(f"{hour}:{minute} -> wysyłam pobrane statystyki")

            generate_forecast_image()
            generate_graphs_image()

            await broadcast_stats()


@tasks.loop(hours=1)
async def generate_weather_image():
    generate_forecast_image()
    generate_graphs_image()

    print(f'Wygenerowano obraz - {datetime.datetime.now().hour}:{datetime.datetime.now().minute}')
