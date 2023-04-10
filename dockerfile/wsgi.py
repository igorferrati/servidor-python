'''
def get_namespaces:

Configura credenciais do cluster validadas no POD

Utiliza o client kubernetes para consumir recursos

Coloca em uma lista as informações consumidas

Retorna a lista ou except
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


'''
def app:
Função chama função get_namespaces(), faz uma verificação para enviar ao cabeçalho HTTP.

Desempacota e formatada lista retornada pela função get_namespace e transforma em bytes

response_headers:
    content-type: define o tipo de conteúdo enviado ao navegador
    content-leght: comprimento em bytes, navegador controla quando recebeu todos bytes

retorna body_meta formatado para refresh e título em bytes.
'''
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

