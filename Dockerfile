# syntax=docker/dockerfile:1

FROM python:3.10.0-slim

# --- Установка системных зависимостей для Playwright, Allure CLI и JRE ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    zip \
    wget \
    openjdk-11-jre-headless \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libxshmfence1 \
    ca-certificates \
    fonts-liberation \
    libxss1 \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя с UID/GID 1001
RUN groupadd -g 1001 appuser && useradd -m -u 1001 -g appuser appuser

WORKDIR /app

# Копируем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Установка Playwright и браузеров
RUN python -m playwright install --with-deps

# Кэш браузеров для non-root
RUN mkdir -p /home/appuser/.cache && \
    if [ -d /root/.cache/ms-playwright ]; then \
        cp -r /root/.cache/ms-playwright /home/appuser/.cache/ && \
        chown -R appuser:appuser /home/appuser/.cache/ms-playwright; \
    fi

# Копируем проект
COPY pytest.ini ./
COPY pages ./pages
COPY tests ./tests

# Устанавливаем Allure CLI
RUN wget -qO /tmp/allure.zip https://github.com/allure-framework/allure2/releases/download/2.21.0/allure-2.21.0.zip && \
    unzip /tmp/allure.zip -d /opt/ && \
    ln -s /opt/allure-2.21.0/bin/allure /usr/local/bin/allure && \
    rm /tmp/allure.zip

# Права на рабочую директорию
RUN chown -R appuser:appuser /app

# Переключаемся на non-root пользователя
USER appuser

ENV PLAYWRIGHT_HEADLESS=1

# Команда по умолчанию при старте контейнера: сначала тесты (с генерацией отчетов Allure, прописано в pytest.ini), потом Allure сервер.
CMD bash -c "pytest && allure serve allure-results --host 0.0.0.0 --port 8080"

