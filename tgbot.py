
from telethon import TelegramClient, events
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('TOKEN')

client = TelegramClient('session_name',
                        api_id, api_hash).start(bot_token=bot_token)


def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).astimezone().strftime(
        '%Y-%m-%d %H:%M:%S %Z')


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    try:
        name = event.sender.first_name
        await event.respond('Привет {}, введи @никнейм пользователя, чтобы получить информацию)'.format(name))
    except Exception:
        pass


@client.on(events.NewMessage)
async def get_user_info(event):
    username = event.raw_text.strip()
    try:
        user = await client.get_entity(username)
        user_info = f"Имя пользователя: {user.username}\n"
        user_info += f"Имя: {user.first_name}\n"
        user_info += f"Фамилия: {user.last_name}\n"
        user_info += f"ID пользователя: {user.id}\n"
        
        # Сохранение фотографии аватарки, если она есть
        photos = await client.get_profile_photos(user.id, limit=5)
        
        # Сохранение фотографий и отправка их
        for i, photo in enumerate(photos):
            photo_file = await client.download_media(photo)
            photo_path = f"{username}_profile_photo_{i}.jpg"
            os.rename(photo_file, photo_path)
            await event.respond(file=photo_path)
        
        user_info += f"Количество фотографий профиля: {len(photos)}"
        await event.respond(user_info)
    except Exception as e:
        pass
client.run_until_disconnected()

