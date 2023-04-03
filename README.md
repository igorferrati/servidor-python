# Servidor Python :snake:

## WSGI - Web Server Gateway Interface

Criação de um servidor que lista namespace de um cluster com topologia:

* NGINX como proxy reversa
* Gunicorn como servidor HTTP 
* Cluster Role / Service Account para acesso da API

---

:file_folder: wsgi
* Arquivo helm

:file_folder: dockerfile
* Build imagem docker
* arquivos.py

---

## Config Nginx

```
server {
      listen 80 default_server;
      listen [::]:80 default_server;
      server_name server-wsgi-py;

      location / {
          proxy_pass http://localhost:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      }
      }
```
```location / ``` encaminha o localhost (onde subir a imagem) para porta 8000 da qual teremos Gunicorn rodando um WSCGI, o mesmo realiza o comando ```kubectl get ns``` no cluster do qual a aplicação está e devolve para o site estátigo do nginx.

* A aplicação possuí acesso para listar os namespaces atraves de um ServiceAccount e ClusterRole/ClusterRoleBinding.

## Python / Dockerfile

* O build da imagem cria as dependências necessárias para utilização do Gunicorn
* O arquivo requirements.txt funciona como uma lista de depêndencias 
* O comando ```python3 -m pip install -r requirements.txt``` instala o que for listado em requirements.txt de acordo com a versão especificada.

## ServiceAccount / ClusterRole / ClusterRoleBinding

Para acesso do cluster do qual deseja rodar a imagem é necessário criar uma RBAC de acesso e vincular um serviceaccount ao tipo de permissão desejada.

* No helm temos o seguinte exemplo, partindo do principio que já temos um namespace em questão para a aplicação e devemos víncular o helm a um namespace:

``` helm install <realease> <chart-name> -n <namespace>```

* Este namespace já prédefinido deve no ClusterRoleBinding

```
clusterrolebind:
  name: sa-get-ns
  subjects:
  - kind: ServiceAccount
    name: get-app-desafio     #name sa
    namespace: app-desafio
  roleRef:
    kind: ClusterRole
    name: get-namespaces      #name role
    apiGroup: rbac.authorization.k8s.io
```
