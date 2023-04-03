'''
Função incia uma aplicação WSGI (Web Server Gateway Interface)

environ: dic com informações da requisição HTTP
start_response: func que envia resposta HTTP de volta ao cliente, recebe
                código de status HTTP e dic de cabeçalhos HTTP.
data: variável resposta simples em bytes
status: variável com código de confirmação ok HTTP
response_headers: lista de tuplas com cabeçalhos HTTP
return: iteração o que contém em data
'''
import subprocess as sub

def app(environ, start_response):
    ns = sub.check_output(['kubectl', 'get', 'ns'])
    data = ns           #em bytes
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data.decode()])

