import datetime
import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

# Load environment variables from a .env file
load_dotenv()

# Initialize Telegram client with API credentials and start session
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('TOKEN')

client = TelegramClient('session_name',
                        api_id, api_hash).start(bot_token=bot_token)


def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(
        timestamp,
        datetime.timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    name = event.sender.first_name
    await event.respond('Привет {}, введи @никнейм пользователя, '
                        'чтобы получить информацию:)'.format(name))


@client.on(events.NewMessage)
async def get_user_info(event):
    username = event.raw_text.strip()
    user = await client.get_entity(username)
    user_info = f"Имя пользователя: {user.username}\n"
    user_info += f"Имя: {user.first_name}\n"
    user_info += f"Фамилия: {user.last_name}\n"
    user_info += f"ID пользователя: {user.id}\n"
    user_info += f"Номер телефона: {user.phone}\n"

    # Download profile photos and send them
    photos = await client.get_profile_photos(user.id)
    for i, photo in enumerate(photos):
        photo_file = await client.download_media(photo)
        photo_path = f"{username}_profile_photo_{i}.jpg"
        os.rename(photo_file, photo_path)
        await event.respond(file=photo_path)

    user_info += f"Количество фотографий профиля: {len(photos)}"
    await event.respond(user_info)
client.run_until_disconnected()
