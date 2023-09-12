# First stage:
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate

# Second stage:
FROM builder AS final

RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
