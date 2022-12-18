import time
from aiogram import Bot, Dispatcher, executor, types
from pytube import YouTube
from googleapiclient.discovery import build
import json
from time import sleep
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime as dt
import requests


token = ''
api = ''
weather_key = ''
download_folder = ''

bot = Bot(token=token)
dp = Dispatcher(bot)

def get_service():
    service = build('youtube', 'v3', developerKey=api)
    return service

def get_video_info(video_id):
    r = get_service().videos().list(id=video_id, part='snippet, statistics').execute()
    return r

@dp.message_handler(commands='start')
async def first_of_all(message):
    print(message)
    await bot.send_message(message.chat.id, f'Привет {message["from"]["first_name"]}, я YouTube-бот,\nпомогу тебе скачать видео из ютуба и вывести статистику ')
    await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEGwTVjk7ZWMCxnbgZGH5Mff-Fiu1Vz3QACeQUAAjbsGwWk_F_hIHgbZisE')
    await bot.send_message(message.chat.id, 'отправь ссылку на видео: ')


@dp.message_handler()
async def get_message_and_send_info(message):
    link = message.text
    yt = YouTube(link)
    print(message)
    print(yt)
    if message.text.startswith == 'https://www.youtube.com/' or 'https://youtu.be/':
        await bot.send_message(message.chat.id, f'Скачиваю видео: *{yt.title}* \n'
                                                f'Автор : [{yt.author}]({yt.channel_id}', parse_mode='Markdown')
        await download_youtube_video(link, message, bot)
    else:
        await bot.send_message(message.chat.id, f'хммм, не похоже на ссылку с YouTube.....')
        await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEGzl1jl7qCjejyxkchtpbxsyGrhm6nmAACjQMAAjbsGwU4uEquYGopGywE')


async def download_youtube_video(link, message, bot):
    yt = YouTube(link)
    stream = yt.streams.filter(progressive=True, file_extension='mp4')
    stream.get_highest_resolution().download(f'{download_folder}', f'{message.chat.id}_{yt.title}')
    with open(f'{download_folder}{message.chat.id}_{yt.title}', 'rb') as video:
        publication_date = get_video_info(link.split('=')[1])['items'][0]['snippet']['publishedAt']
        print(get_video_info(link.split('=')[1])['items'][0]['statistics'])
        menu = InlineKeyboardMarkup(row_width=2)
        view_count = get_video_info(link.split('=')[1])['items'][0]['statistics']['viewCount']
        like_count = get_video_info(link.split('=')[1])['items'][0]['statistics']['likeCount']
        comment_count = get_video_info(link.split('=')[1])['items'][0]['statistics']['commentCount']
        viewers = InlineKeyboardButton(text=f'Просмотры: {view_count}', callback_data='viewers')
        comments = InlineKeyboardButton(text=f'Комментарии: {comment_count}', callback_data='comments')
        likes = InlineKeyboardButton(text=f'Лайки: {like_count}', callback_data='likes')
        menu.insert(likes)
        menu.insert(comments)
        menu.insert(viewers)
        try:
            await bot.send_video(message.chat.id, video, caption=f'Дата Выхода:*{publication_date}*', parse_mode='Markdown', reply_markup=menu)
        except Exception as e:
            upload_file = open(f'{download_folder}{message.chat.id}_{yt.title}', 'rb')

            await bot.send_message(message.chat.id, 'К сожалению Видео слишком тяжелое, телеграм такой вес не поддерживает :))')
            await bot.send_message(message.chat.id, f'Вот статистика: \n'
                                                    f'Просмотры: {view_count} \n'
                                                    f'Комментарии: {comment_count} \n'
                                                    f'Лайки: {like_count}')

@dp.message_handler(content_types=['location'])
async def send_weather_to_location(message: types.Message):
    latitude = message["location"]["latitude"]
    longitude = message["location"]["longitude"]
    weather = (requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={weather_key}').json())
    print(weather)
    await bot.send_message(message.chat.id, f"Температура в данный момент: {round(weather['main']['temp'] - 273.15)}\n"
                                            f"Ощущается как: {round(weather['main']['feels_like'] - 273.15)}\n"
                                        f'Восход солнца в: {dt.datetime.fromtimestamp(weather["sys"]["sunrise"])} \n'
                                            f'Заход солнца в: {dt.datetime.fromtimestamp(weather["sys"]["sunset"])}')




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
