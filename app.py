from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from spyne.protocol.soap import Soap11
from spyne import rpc, ServiceBase, \
    Integer, Unicode, Boolean
import logging
from pyramid.config import Configurator
from pyramid.view import view_config
from spyne.util.simple import pyramid_soap11_application
logging.basicConfig(level=logging.DEBUG)

DB = [{
    "full_name": "luis correa",
    "card_number": 5412750123450987,
    "cvv_number": 123,
    "type": "visa",
    "expiration_month": 12,
    "expiration_year": 2022
}]


class PaymentService(ServiceBase):
    @rpc(Unicode, Integer, Integer, Unicode, Integer, Integer, _returns=Boolean)
    def check_payment(ctx, full_name, card_number, cvv_number, type, expiration_month, expiration_year):
        input = {
            "full_name": full_name.lower(),
            "card_number": card_number,
            "cvv_number": cvv_number,
            "type": type.lower(),
            "expiration_month": expiration_month,
            "expiration_year": expiration_year
        }
        for card in DB:
            if input == card:
                return True
        return False


soapApp = view_config(route_name="home")(
    pyramid_soap11_application([PaymentService], tns='visa.mastercard.payment', ))

if __name__ == '__main__':
    settings = {}
    settings['debug_all'] = True
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()
