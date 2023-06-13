import os
from flask import Flask
from flask_script import Server
from abc import ABCMeta
#from aiprofile_api.routes import aiTest
from aiprofile_api.routes.data_dump import postgreetest
#from aiprofile_api.utils import MongoEncoder, Logging
from aiprofile_api.configs import config_from_ini
from aiprofile_api.utils import Logging, MongoEncoder


def create_app():
    app = Flask(__name__)
    app.json_encoder = MongoEncoder
    # load config from config.ini file
    config_from_ini(app)

    # register our blueprints

    app.register_blueprint(postgreetest)
    return app


class HookServer(Server, metaclass=ABCMeta):

    def __call__(self, app, *args, **kwargs):
        # Hint: Here you could manipulate app whatever you wanna start before start the server
        app.config.cache = dict()

        # if current env is in local use flask server
        if app.config["ENV"] == os.getenv("ENV"):
            # when cache is filled then start the server
            # override default value from base class
            kwargs["host"] = app.config["HOST"]
            kwargs["port"] = app.config["PORT"]
            kwargs["use_reloader"] = app.config["RELOADED"]
            return Server.__call__(self, app, *args, **kwargs)

        # otherwise use wsgi server instead
        from gevent.pywsgi import WSGIServer
        http_server = WSGIServer((app.config["HOST"], app.config["PORT"]), app, log=Logging.get_logger())
        Logging.info("Listening at: {}:{}".format(app.config["HOST"], app.config["PORT"]))
        return http_server.serve_forever()