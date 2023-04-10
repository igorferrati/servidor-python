'''
Função incia uma aplicação WSGI e usa python para consumir dados da API

environ: dicionário com informações da requisição HTTP
start_response: func que envia resposta HTTP de volta ao cliente, recebe
                código de status HTTP e dicionário de cabeçalhos HTTP.

ns e get_ns = variáveis para manipulação e tratamento dos dados consumidos
data: variável de resposta de dados
status: variável com código de confirmação ok HTTP

response_headers:
    content-type: define o tipo de conteúdo enviado na navegador (texto simples)
    content-leght: comprimento em bytes, navegador controla quando recebeu todos bytes
    refresh: requisição de atualização de 5 segundos

return: iteração o que contém em data
'''
from kubernetes import client, config

def get_namespaces():
    try:
        # Load Kubernetes config file
        config.load_incluster_config()

        # Create Kubernetes API cliente
        ns = client.CoreV1Api()

        ns_list = ns.list_namespace()
        get_ns = []

        for namespace in ns_list.items:
            get_ns.append(namespace.metadata.name)

        return get_ns

    except Exception as erro:
        return str(erro)


def app(environ, start_response):

    namespaces = get_namespaces()

    if isinstance(namespaces, list):
        status = '200 OK'
        body = b''
        for name in namespaces:
            body += f'<pre>{name}</pre>'.encode()
        
        
    else:
        status = '500 Internal Server Error'
        body = str(namespaces).encode("utf-8")

    response_headers = [
        ('Content-type', 'text/html'),
        ('Content-Length', str(len(body)))
    ]

    meta_tag = b'<h2>namespaces:</h2> <meta http-equiv="refresh" content="5">'
    body_meta = meta_tag + body

    start_response(status, response_headers)
    return [body_meta]