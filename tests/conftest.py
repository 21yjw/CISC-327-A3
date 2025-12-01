import pytest
from app import create_app
import threading
import socket
from werkzeug.serving import make_server

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    return app


#this complexity is to make it work on windows(something about multithreading)
@pytest.fixture(scope="session")
def live_server_url(app):
    # Bind to an open port
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()

    server = make_server('127.0.0.1', port, app)

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    url = f"http://127.0.0.1:{port}"

    yield url

    server.shutdown()
    thread.join()