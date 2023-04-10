# Servidor Python :snake:

## WSGI - Web Server Gateway Interface

Criação de um servidor que lista namespace de um cluster com topologia:

* NGINX como proxy reversa
* Gunicorn como servidor HTTP 
* Cluster Role / Service Account para acesso da API
* Implantação via helm
---

:file_folder: wsgi
* chart helm

:file_folder: dockerfile
* build imagem docker
* arquivos.py

---

## Config Nginx

Configuração nginx (port 80) com gunicorn (port 8000)

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
```location / ``` encaminha o localhost (onde estiver a image) para porta 8000 (Gunicorn).

## Python / Dockerfile

* O build da imagem cria as dependências
* O arquivo requirements.txt possui as bibliotecas necessárias
* O comando ```python3 -m pip install -r requirements.txt``` configura qual o pip install de acordo com a versão especificada
* É utilizado o [Kubernetes Python Client](https://github.com/kubernetes-client/python) API para consumir recursos do cluster

## ServiceAccount / ClusterRole / ClusterRoleBinding

* A aplicação deve possuir acesso para listar os namespaces.

Para acesso do cluster do qual deseja rodar a imagem é necessário criar uma RBAC de acesso e vincular um serviceaccount ao tipo de permissão desejada.

* No helm temos o seguinte exemplo, partindo do principio que já temos um namespace em questão para a aplicação e devemos víncular o helm a um namespace:

``` helm install <release> <chart-name> -n <namespace>```

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


