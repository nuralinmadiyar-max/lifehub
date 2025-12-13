# 1️⃣ Берём официальный Python
FROM python:3.11-slim

# 2️⃣ Рабочая директория внутри контейнера
WORKDIR /app

# 3️⃣ Копируем зависимости
COPY requirements.txt .

# 4️⃣ Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Копируем код backend
COPY . .

# 6️⃣ Открываем порт
EXPOSE 8000

# 7️⃣ Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]