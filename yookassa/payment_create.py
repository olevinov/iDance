from yookassa import Payment
import uuid
import argparse
import sys
from datetime import datetime
import payment_config

# Это находится в payment_config.py
# Configuration.account_id = 294043
# Configuration.secret_key = "test_Pa9IbaLN9i9ragcXEvuT-is_VFp1e9wawtvrws2Mul8"

parser = argparse.ArgumentParser(description='Test yookassa payment create.')
parser.add_argument('-a', '--amount', type=int, default=100, help='amount of payment (default: %(default)s)')
parser.add_argument('-o', '--orderid', type=str, default="none", help='order ID (default: %(default)s)')

args = parser.parse_args()

idempotence_key = str(uuid.uuid4())
payment_date_time = datetime.now().strftime("%d.%m/.%Y %H:%M:%S")

try:
    payment = Payment.create({
        "amount": {
            "value": f"{args.amount}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"http://localhost:8000?idempotence_key={idempotence_key}&order_id={args.orderid}"
        },
        "capture": True,
        "description": f"Заказ № {args.orderid} от {payment_date_time} ({idempotence_key})"
    }, idempotence_key)
except Exception as err:
    sys.stderr.write(f"Exception {err=}, {type(err)=}")
    exit(1)

# Возвратит url для перевода пользователя на страницу оплаты вида
# https://yoomoney.ru/checkout/payments/v2/contract?orderId=2d0e71f9-000f-5000-a000-1e6812687f83
# в orderId находится Идентификатор платежа
# Позже по этому идентификатору мы будем проверять статус платежа (оплачен или не оплачен)

payment_id = payment.id
confirmation_url = payment.confirmation.confirmation_url

with open("payment_id.txt", "w") as p_file:
    p_file.write(f'{idempotence_key} {payment_id}')

print(f"{payment_id=}, {confirmation_url=}")
