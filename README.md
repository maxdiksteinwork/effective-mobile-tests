# Effective Mobile UI Tests

Автоматизация UI-тестирования главной страницы сайта [https://effective-mobile.ru](https://effective-mobile.ru) с использованием **Python 3.10**, **Playwright**, **pytest**, **Allure** и **Docker**.

## Структура проекта

```
effective-mobile-tests/
├── tests/                  # UI-тесты (pytest + allure)
│   └── test_main_page.py
├── pages/                  # Page Object Model
│   └── main_page.py
├── Dockerfile              # Docker-сборка тестов
├── pytest.ini              # Конфигурация pytest
├── requirements.txt        # Зависимости проекта
├── README.md               # Инструкция (этот файл)
└── .gitignore
```

---

## Запуск локально

### Требования

- Python 3.10+
- Allure Commandline (CLI)

### Установка Python 3.10+

#### Windows:

- [Скачать Python 3.10](https://www.python.org/downloads/release/python-3100/)
- При установке **обязательно** поставить галочку **"Add Python to PATH"**
- После установки проверить версию:

```bash
python --version
```

#### Linux:


```bash
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev -y
python3.10 --version
```

### Установка Allure CLI

> ⚠️ **Важно**: Для работы Allure необходим установленный Java Runtime (JRE)!

#### Windows:

1. Установить [Java JDK или JRE](https://adoptium.net/en-GB/temurin/releases/) (например, Temurin 17)
2. Убедиться, что переменная среды `JAVA_HOME` прописана, а путь `bin` добавлен в `PATH`
3. Скачать Allure CLI с [официальной страницы](https://github.com/allure-framework/allure2/releases)
4. Распаковать архив в удобное место (например, `C:\Tools\allure`)
5. Добавить путь к папке `bin` в переменную среды `PATH` (например, `C:\Tools\allure\bin`)
6. Перезапустить терминал
7. Проверить установку:

```bash
allure --version
```

##### Проверка и установка переменной JAVA\_HOME

Если переменной `JAVA_HOME` нет:

1. Найти путь, где установлена Java, например:
   ```
   C:\Program Files\Eclipse Adoptium\jdk-17.0.11.9-hotspot
   ```
2. Открыть: **Панель управления → Система → Дополнительные параметры системы → Переменные среды**
3. В разделе «Системные переменные» нажать **Создать**:
   - Имя переменной: `JAVA_HOME`
   - Значение: полный путь к установленной Java
4. Найти переменную `Path`, нажать **Изменить**, добавить строку:
   ```
   %JAVA_HOME%\bin
   ```
5. Перезапустить терминал (или систему, если не помогает)
   
#### Linux:

```bash
sudo apt install default-jre -y  # Установка Java
wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz
sudo tar -zxvf allure-2.27.0.tgz -C /opt/
sudo ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure
allure --version
```

### Установка зависимостей и запуск тестов

1. Клонировать репозиторий:

```bash
git clone https://github.com/maxdiksteinwork/effective-mobile-tests.git
cd effective-mobile-tests
```

2. Создать виртуальное окружение и установить зависимости

#### Windows (CMD или PowerShell):

```powershell
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
playwright install
```
> ⚠️ Если используется **Git Bash** в Windows, для активации окружения используйте:
>
> ```bash
> source venv/Scripts/activate
> ```
> 
#### Linux/macOS:

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
playwright install
```

3. Запустить тесты и сгенерировать отчёт Allure:

```bash
pytest
```

Тесты будут запущены с параметрами, указанными в `pytest.ini`:

```ini
addopts = -n auto --alluredir=allure-results --clean-alluredir
```

#### Описание параметров:

- `-n auto` — запуск тестов в несколько потоков (параллельно), где `auto` означает, что количество потоков будет выбрано автоматически на основе количества ядер процессора.
- `--alluredir=allure-results` — сохраняет результаты тестирования в директорию `allure-results`, которая используется для генерации отчета Allure.
- `--clean-alluredir` — очищает папку `allure-results` перед запуском тестов, чтобы исключить попадание устаревших данных в отчет.

#### Просмотр отчета:

После завершения тестов выполнить команду:

```bash
allure serve allure-results
```

Это откроет интерактивный отчет в браузере.

---

## Запуск в Docker

### Требования

- Docker

### Установка Docker

#### Windows / macOS:

- [Установить Docker Desktop](https://docs.docker.com/desktop/)
- Перезагрузить систему после установки
- Проверить установку:

```bash
docker --version
```

#### Linux (например, Ubuntu):

```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl enable docker --now
sudo usermod -aG docker $USER
newgrp docker

docker --version
```

### Сборка и запуск проекта

1. Клонировать репозиторий:

```bash
git clone https://github.com/maxdiksteinwork/effective-mobile-tests.git
cd effective-mobile-tests
```

2. Собрать Docker-образ:

```bash
docker build -t effective-mobile-playwright-test .
```

3. Запустить тесты и открыть отчет в браузере:

```bash
docker run --rm -p 8080:8080 effective-mobile-playwright-test bash -c "pytest && exec allure serve allure-results --host 0.0.0.0 --port 8080"
```

Перейти в браузере по адресу [http://localhost:8080/](http://localhost:8080/) для просмотра отчёта Allure.

---

## Контакты

При возникновении вопросов отправить письмо на [maxdikstein.work@gmail.com](mailto\:maxdikstein.work@gmail.com)

