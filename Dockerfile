FROM python:3.10.9-slim-bullseye
RUN mkdir /app
WORKDIR /app
ADD requirements.txt .
ADD gunicorn.conf.py .
ADD gunicorn.logging.conf .
COPY ./backend backend
COPY ./icons icons
RUN pip install -r requirements.txt && \
    pip install gunicorn==20.1.0
EXPOSE 8930
ENV TZ Asia/Tokyo
CMD ["gunicorn", "--config", "/app/gunicorn.conf.py", "--log-config", "/app/gunicorn.logging.conf"]
