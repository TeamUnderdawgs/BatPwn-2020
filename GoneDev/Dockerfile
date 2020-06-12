FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

# make port 8000 available to the world outside
EXPOSE 8002

#CMD ["ls -la /usr/bin/"]

CMD ["python3", "app.py"]
#CMD ["gunicorn", "-b", "0.0.0.0:8002", "app:app", "-w", "10"]

#CMD ["gunicorn -b 0.0.0.0:8000 app:app -w 10"]
