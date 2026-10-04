"""Bounded text/binary echo and deliberate close paths on loopback."""

from websockets.exceptions import ConnectionClosed
from websockets.sync.server import serve


def echo(connection):
    try:
        for message in connection:
            if message == "close":
                connection.close(1000, "demo complete")
                break
            if message == "error":
                connection.close(1011, "intentional demo failure")
                break
            connection.send(message)
    except ConnectionClosed:
        pass


def make_server(port=18428):
    return serve(echo, "127.0.0.1", port, max_size=32768, max_queue=8,
                 open_timeout=5, close_timeout=2)
