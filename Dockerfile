FROM python:rc-slim

COPY requirements.txt ./

RUN pip3 install -r /requirements.txt 


WORKDIR /app

COPY /app /app

EXPOSE 5000

CMD ["/bin/bash", "gunicorn.sh"]