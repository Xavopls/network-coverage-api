FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Expose port dynamically
ARG DJANGO_PORT=8000
ENV DJANGO_PORT=${DJANGO_PORT}.

# Environment variables for superuser creation
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=1234

# Entrypoint script
COPY scripts/init.sh /app/scripts/init.sh
RUN chmod +x /app/scripts/init.sh

# Start server with migrations and superuser creation
ENTRYPOINT ["sh", "/app/scripts/init.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:${DJANGO_PORT}"]
