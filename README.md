# Приветствие

Добро пожаловать, пользователь! Для запуска данного сервиса нужно выполнить 
несколько последовательных действий:


## Создание и активация виртуального окружения
Перейдите в корень проекта `flask_todo_app/` и выполните последовательно две команды:
```bash
$ python3 -m venv venv
$ source venv/bin/activate  # Для Windows используйте venv\Scripts\activate
```

## Установить зависимости
Для этого выполни в консоли следующую команду
```bash
$ pip install -r requirements.txt
```

## Создать базу данных
Для этого потребуется выполнить следующие команды:
```bash
    $ mkdir -p instance
    $ flask db upgrade
```

## Установить SECRET_KEY в переменную окружения, либо проставить значение по умолчанию в файле app/__init__.py
```python
def create_app():
    load_dotenv()
    new_app = Flask(__name__)
    new_app.secret_key = os.getenv("SECRET_KEY") # вот в этом месте
```