    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            color: #333;
        }
        code {
            background: #f4f4f4;
            padding: 2px 4px;
            border-radius: 4px;
            color: #c7254e;
        }
        pre {
            background: #f4f4f4;
            padding: 10px;
            border-radius: 10px;
            overflow: auto;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Музыкальный загрузчик и Телеграм-бот</h1>
        <p>Этот проект включает в себя веб-приложение на основе FastAPI и Телеграм-бота для скачивания музыки с YouTube и её отображения в веб-интерфейсе. Пользователь может ввести название трека, система скачает его с YouTube, конвертирует в формат MP3 и отобразит на веб-странице для дальнейшего прослушивания или скачивания. Телеграм-бот интегрирован для дополнительного взаимодействия с пользователями.</p>
        
        <h2>Структура проекта</h2>
        <ul>
            <li><strong>api</strong>: Основной модуль веб-приложения.
                <ul>
                    <li><code>database.py</code>: Содержит функции для работы с базой данных.</li>
                    <li><code>download_music.py</code>: Модуль для скачивания музыки с YouTube.</li>
                    <li><code>main.py</code>: Основной файл приложения, инициализирующий сервер.</li>
                    <li><code>models.py</code>: Описание моделей базы данных.</li>
                    <li><code>registration.py</code>: Модуль для обработки регистрации пользователей.</li>
                    <li><code>schemas.py</code>: Содержит Pydantic схемы для валидации данных.</li>
                    <li><code>send_password.py</code>: Модуль для отправки пароля пользователям.</li>
                </ul>
            </li>
            <li><strong>media</strong>: Директория для хранения загруженных файлов.
                <ul>
                    <li><code>123</code>: Пример папки с файлами пользователя.
                        <ul>
                            <li>Black Holes Explained - From Formation to Death.mp4</li>
                            <li>New Born.mp3</li>
                            <li>New Born.mp4</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li><strong>templates</strong>: Директория для HTML-шаблонов.
                <ul>
                    <li><code>base.html</code>: Базовый шаблон для страницы.</li>
                    <li><code>index.html</code>: Главная страница с формой для поиска музыки.</li>
                    <li><code>login.html</code>: Страница входа в систему.</li>
                    <li><code>personal_area.html</code>: Личный кабинет пользователя с отображением загруженной музыки.</li>
                </ul>
            </li>
            <li><strong>tg_bot</strong>: Модуль Телеграм-бота.
                <ul>
                    <li><code>.env</code>: Конфигурационный файл для хранения переменных окружения.</li>
                    <li><code>bot.py</code>: Основная логика работы Телеграм-бота.</li>
                    <li><code>main.py</code>: Файл для запуска бота.</li>
                    <li><code>test.db</code>: База данных для хранения информации о пользователях.</li>
                </ul>
            </li>
            <li><code>requirements.txt</code>: Файл зависимостей проекта.</li>
        </ul>
        
        <h2>Установка и запуск проекта</h2>
        <h3>1. Клонирование репозитория</h3>
        <pre><code>git clone https://github.com/ваше_имя/имя_репозитория.git
cd tg_vk_api_for_pars</code></pre>
        
        <h3>2. Установка зависимостей</h3>
        <p>Создайте и активируйте виртуальное окружение:</p>
        <pre><code>python -m venv venv
source venv/bin/activate  # Для Unix-подобных систем
venv\Scripts\activate  # Для Windows</code></pre>
        <p>Установите зависимости из файла <code>requirements.txt</code>:</p>
        <pre><code>pip install -r requirements.txt</code></pre>
        
        <h3>3. Настройка переменных окружения</h3>
        <p>Создайте файл <code>.env</code> в директории <code>tg_bot</code> и заполните его необходимыми переменными окружения. Пример:</p>
        <pre><code>TELEGRAM_TOKEN=&lt;Ваш_Telegram_токен&gt;</code></pre>
        
        <h3>4. Запуск веб-приложения</h3>
        <p>Запустите сервер:</p>
        <pre><code>uvicorn api.main:app --reload</code></pre>
        <p>Откройте в браузере <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a>, чтобы увидеть главную страницу приложения.</p>
        
        <h3>5. Запуск Телеграм-бота</h3>
        <p>Перейдите в директорию <code>tg_bot</code> и запустите бота:</p>
        <pre><code>python main.py</code></pre>
        
        <h2>Функционал проекта</h2>
        <h3>Веб-приложение</h3>
        <p><strong>Загрузка музыки</strong>: Введите название трека в форму на главной странице и нажмите "Download". Система скачает трек с YouTube, конвертирует его в MP3 и отобразит в личном кабинете пользователя.</p>
        <p><strong>Личный кабинет</strong>: Содержит список всех загруженных треков с возможностью их прослушивания и скачивания.</p>
        
        <h3>Телеграм-бот</h3>
        <p>Телеграм-бот позволяет:</p>
        <ul>
            <li>Получать уведомления о завершении загрузки музыки.</li>
            <li>Взаимодействовать с пользователем для выполнения различных команд, таких как регистрация и запрос треков.</li>
        </ul>
        
        <h2>Стек технологий</h2>
        <ul>
            <li><strong>Backend</strong>: FastAPI</li>
            <li><strong>Frontend</strong>: HTML, Jinja2</li>
            <li><strong>Телеграм-бот</strong>: python-telegram-bot</li>
            <li><strong>База данных</strong>: SQLite</li>
            <li><strong>Другие библиотеки</strong>: pytube (для загрузки видео с YouTube)</li>
        </ul>
        
        <h2>Планы на будущее</h2>
        <ul>
            <li>Добавить возможность работы с плейлистами.</li>
            <li>Расширить функционал Телеграм-бота.</li>
            <li>Улучшить интерфейс пользователя и добавить поддержку других видео- и аудио-сервисов.</li>
        </ul>
        
        <h2>Вклад и разработчики</h2>
        <p>Если вы хотите внести вклад в проект, пожалуйста, создайте pull request или откройте issue для обсуждения.</p>
        
        <h2>Лицензия</h2>
        <p>Этот проект лицензирован под <a href="https://opensource.org/licenses/MIT">MIT License</a>.</p>
        
        <p><strong>Спасибо за использование нашего проекта!</strong></p>
        
        <h2>Скриншоты</h2>
        <p><img src="path/to/your/image.png" alt="Структура проекта"></p>
    </div>
</body>
</html>

