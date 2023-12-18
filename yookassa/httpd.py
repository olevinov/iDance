from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse, parse_qs
from yookassa import Payment
from yookassa.domain.response import PaymentResponse

import sys
import payment_config

def getPaymentDataFromFile():
    idempotence_key = None
    payment_id = None
    with open("payment_id.txt", "r") as p_file:
        data = p_file.readline().split()
        if len(data) > 1:
            idempotence_key = data[0]
            payment_id = data[1]
    return idempotence_key, payment_id

def getPayment(payment_id: str) -> PaymentResponse:
    try:
        payment = Payment.find_one(payment_id)
        return payment
        #print(payment.json())
    except Exception as err:
        sys.stderr.write(f"Exception {err=}, {type(err)=}")
    return None

def getQueryParam(path: str, param_name: str) -> str:
    param_list = parse_qs(urlparse(path).query).get(param_name, None)
    return param_list[0] if isinstance(param_list, list) and len(param_list) > 0 else None

class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode())
        self.wfile.write('<body>'.encode())
        self.wfile.write('<p>Был получен GET-запрос'.encode())
        self.wfile.write(f'<p>{self.path}'.encode())
        idempotence_key = getQueryParam(self.path, 'idempotence_key')
        if idempotence_key:
            self.wfile.write(f'<p>idempotence_key={idempotence_key}'.encode())
        order_id = getQueryParam(self.path, 'order_id')
        if order_id:
            self.wfile.write(f'<p>order_id={order_id}'.encode())
        payment_idempotence_key, payment_id = getPaymentDataFromFile()
        if idempotence_key != None and idempotence_key == payment_idempotence_key:
            self.wfile.write(f'<p>payment_id={payment_id}'.encode())
        else:
            self.wfile.write(f'<p>idempotence_key mismatch {idempotence_key} {payment_idempotence_key}'.encode())
        payment = getPayment(payment_id)
        if payment and payment.id == payment_id and payment.status == 'succeeded':
            self.wfile.write('<p>payment SUCCEEDED'.encode())
        else:
            self.wfile.write('<p>payment FAILED'.encode())
        if payment:
            self.wfile.write(f'<p>{payment.json()}'.encode())
        self.wfile.write('</body></html>'.encode())

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

run(handler_class=HttpGetHandler)
