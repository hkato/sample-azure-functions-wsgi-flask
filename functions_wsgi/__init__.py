import logging

import azure.functions as func

from flask_app.app import app


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # WSGI Application
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)
