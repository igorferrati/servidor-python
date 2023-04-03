FROM nginx:stable-alpine-slim

COPY default.conf /etc/nginx/conf.d/
COPY setup.py /
COPY requirements.txt /
COPY wsgi.py /app/


RUN  apk update && \
     apk add curl && \
     curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
     chmod +x kubectl && \
     install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
     apk add python3 && \
     python3 -m ensurepip --upgrade && \
     python3 -m pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python3", "./setup.py"]
