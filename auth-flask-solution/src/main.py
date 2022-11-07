from gevent import monkey

monkey.patch_all()
from main_sync import app
from gevent.pywsgi import WSGIServer

http_server = WSGIServer(('', app.config['AUTH_PORT']), app)
http_server.serve_forever()
