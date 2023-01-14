FROM python:3.10.9-slim-bullseye
RUN mkdir /app
WORKDIR /app
ADD requirements.txt .
COPY ./backend backend
COPY ./icons icons
RUN pip install -r requirements.txt
EXPOSE 8930
CMD ["python", "-m", "backend.app"]
