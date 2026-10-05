"""Start selected local transports; Ctrl+C closes task-owned servers."""

import argparse
import json
import threading
from contextlib import ExitStack


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", choices=("http", "websocket", "grpc", "all"), default="all")
    parser.add_argument("--http-port", type=int, default=18427)
    parser.add_argument("--websocket-port", type=int, default=18428)
    parser.add_argument("--grpc-port", type=int, default=18429)
    args = parser.parse_args()
    if any(not 1 <= value <= 65535 for value in (args.http_port, args.websocket_port, args.grpc_port)):
        parser.error("ports must be 1..65535")
    endpoints, threads = {}, []
    with ExitStack() as stack:
        if args.protocol in ("http", "all"):
            from http_server import make_server
            server = stack.enter_context(make_server(args.http_port))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            stack.callback(server.shutdown)
            threads.append(thread)
            endpoints["http"] = f"http://127.0.0.1:{server.server_port}"
        if args.protocol in ("websocket", "all"):
            from websocket_server import make_server
            server = stack.enter_context(make_server(args.websocket_port))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            threads.append(thread)
            endpoints["websocket"] = f"ws://127.0.0.1:{server.socket.getsockname()[1]}"
        if args.protocol in ("grpc", "all"):
            from grpc_server import make_server
            server, executor, port = make_server(args.grpc_port)
            stack.callback(executor.shutdown, wait=True)
            stack.callback(lambda: server.stop(0).wait(timeout=5))
            server.start()
            endpoints["grpc"] = f"http://127.0.0.1:{port}"
        print(json.dumps({"status": "READY", "endpoints": endpoints}), flush=True)
        try:
            # A timed wait lets Python dispatch Ctrl+C on Windows as well.
            stop = threading.Event()
            while not stop.wait(timeout=0.2):
                pass
        except KeyboardInterrupt:
            pass
    for thread in threads:
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
