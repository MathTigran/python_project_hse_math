# python_project_hse_math


Это телеграмм-бот который позволяет скачивать видео с YouTube, важно понимать, что телеграм разрешает отправлять видео не бесконечно большого размера, 
поэтому если какое-то видео Вы не получили, значит, оно достаточно велико и не проходит через ограничения telegram, 
Прикольная фича: если отправить свою геолокацию (через кнопку в приложении telegram), то бот вернет Вам актуальную температуру и время восхода, захода солнца конкретно по вашей геолокации

Для того чтобы начать пользоваться ботом достаточно будет заменить строки на Ваши:
1. 'token' - токен бота, который получаем при создании бота в https://t.me/BotFather
2. 'api' - ключ доступа api к сервисам googlе, можно получить в https://cloud.google.com, создав проект и получив api_key - это есть то, что нам нужно
3. 'weather_key' - ключ доступа к сервисам openweathermap.org - проходим простую регистрацию и во вкладке 'My Api Keys' получаем заветный ключик доступа к openweathermap.org
4. В 'download_folder' указать путь до папки в которую будут скачиваться видео перед отправкой через бота пользователю
