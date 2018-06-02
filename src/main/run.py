from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from mods_guard.webapp import app
from tornado.options import options
import logging
import logging.config

options.parse_command_line()
logging.info("starting service...")

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(18080)
IOLoop.instance().start()
