FROM nginx:stable-alpine-slim

COPY default.conf /etc/nginx/conf.d/
COPY setup.py /
COPY requirements.txt /
COPY wsgi.py /app/


RUN  apk update && \
     apk add curl && \
     apk add python3 && \
     python3 -m ensurepip --upgrade && \           
     python3 -m pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python3", "./setup.py"]
