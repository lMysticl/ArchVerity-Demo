"""Real TCP roundtrips and negative controls for the demonstration servers."""

import json
from http.cookiejar import CookieJar
import threading
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

import grpc
from google.protobuf import descriptor_pb2
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.sync.client import connect

import grpc_server
import http_server
import websocket_server


class HttpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http_server.make_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def get(self, path):
        with urllib.request.urlopen(self.base + path, timeout=2) as response:
            return json.load(response)

    def test_capture_chain_on_real_http(self):
        first = self.get("/items/42")
        self.assertEqual(first["id"], 42)
        self.assertIs(first["enabled"], True)
        self.assertIsNone(first["optional"])
        data = json.dumps({"id": first["id"]}).encode()
        request = urllib.request.Request(self.base + "/qa-roundtrip", data=data,
                                         headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=2) as response:
            self.assertEqual(json.load(response)["received"], {"id": 42})

    def test_import_targets(self):
        self.assertEqual(self.get("/qa-openapi")["source"], "openapi")
        self.assertEqual(self.get("/health")["status"], "ok")

    def test_dsl_type_and_pointer_inputs_over_real_http(self):
        value = self.get("/dsl-shapes")
        self.assertIs(type(value["id"]), int)
        self.assertIs(type(value["numericString"]), str)
        self.assertIs(value["enabled"], True)
        self.assertIsNone(value["optional"])
        self.assertNotIn("missing", value)
        self.assertEqual(value["items"][0]["id"], 42)
        self.assertEqual(value["a/b"]["~name"], "escaped")

    def test_cookie_and_environment_header(self):
        jar = CookieJar()
        client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        with client.open(self.base + "/cookies/set", timeout=2) as response:
            self.assertTrue(json.load(response)["cookieSet"])
        with client.open(self.base + "/cookies/show", timeout=2) as response:
            self.assertTrue(json.load(response)["hasDemoCookie"])
        jar.clear()
        with client.open(self.base + "/cookies/show", timeout=2) as response:
            self.assertFalse(json.load(response)["hasDemoCookie"])
        request = urllib.request.Request(self.base + "/headers", headers={"X-Demo": "local"})
        with client.open(request, timeout=2) as response:
            self.assertEqual(json.load(response), {"demoHeader": "local", "hasAuthorization": False})

    def test_http_error_and_unknown_route(self):
        for path, status in (("/error", 500), ("/missing", 404), ("/large?bytes=1000001", 400)):
            with self.assertRaises(urllib.error.HTTPError) as failure:
                self.get(path)
            self.assertEqual(failure.exception.code, status)
            failure.exception.close()

    def test_invalid_json_and_request_budget(self):
        for data, status in ((b"{", 400), (b"{}" * 16385, 413)):
            with self.assertRaises(urllib.error.HTTPError) as failure:
                urllib.request.urlopen(urllib.request.Request(self.base + "/qa-roundtrip", data=data), timeout=2)
            self.assertEqual(failure.exception.code, status)
            failure.exception.close()

    def test_redirect_and_large_response(self):
        self.assertEqual(self.get("/redirect")["status"], "ok")
        self.assertEqual(len(self.get("/large?bytes=65536")["data"]), 65536)

    def test_client_timeout_then_next_request(self):
        with self.assertRaises(TimeoutError):
            urllib.request.urlopen(self.base + "/qa-slow?delay_ms=100", timeout=0.01)
        self.assertEqual(self.get("/health")["status"], "ok")


class WebSocketTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = websocket_server.make_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"ws://127.0.0.1:{cls.server.socket.getsockname()[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=5)

    def test_text_and_binary_roundtrip(self):
        with connect(self.url, open_timeout=2) as connection:
            for message in ("ArchVerity", b"\x00\x01demo"):
                connection.send(message)
                self.assertEqual(connection.recv(timeout=2), message)

    def test_normal_close(self):
        with connect(self.url, open_timeout=2) as connection:
            connection.send("close")
            with self.assertRaises(ConnectionClosedOK):
                connection.recv(timeout=2)

    def test_error_close(self):
        with connect(self.url, open_timeout=2) as connection:
            connection.send("error")
            with self.assertRaises(ConnectionClosedError):
                connection.recv(timeout=2)

    def test_message_budget(self):
        with connect(self.url, open_timeout=2) as connection:
            connection.send("x" * 32769)
            with self.assertRaises(ConnectionClosedError):
                connection.recv(timeout=2)


class GrpcTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server, cls.executor, port = grpc_server.make_server(0)
        cls.server.start()
        cls.channel = grpc.insecure_channel(f"127.0.0.1:{port}")
        cls.request_type, cls.reply_type, cls.empty_type = grpc_server.messages()

    @classmethod
    def tearDownClass(cls):
        cls.channel.close()
        cls.server.stop(0).wait(timeout=5)
        cls.executor.shutdown(wait=True)

    def unary(self, method="Say", input_type=None):
        return self.channel.unary_unary(f"/archverity.demo.Echo/{method}",
                                        request_serializer=(input_type or self.request_type).SerializeToString,
                                        response_deserializer=self.reply_type.FromString)

    def test_schema_includes_import_and_stream_flags(self):
        descriptor = descriptor_pb2.FileDescriptorSet.FromString(grpc_server.SCHEMA.read_bytes())
        self.assertEqual({entry.name for entry in descriptor.file}, {"echo.proto", "google/protobuf/empty.proto"})
        service = descriptor.file[-1].service[0]
        methods = {method.name: method for method in service.method}
        self.assertTrue(methods["Watch"].server_streaming)
        self.assertTrue(methods["Upload"].client_streaming)
        self.assertTrue(methods["Chat"].client_streaming and methods["Chat"].server_streaming)

    def test_health_and_unary(self):
        self.assertEqual(self.unary("Health", self.empty_type)(self.empty_type(), timeout=2).text, "ok")
        result = self.unary()(self.request_type(text="demo"), timeout=2)
        self.assertEqual((result.text, result.sequence), ("demo", 1))

    def test_ordered_server_stream(self):
        call = self.channel.unary_stream("/archverity.demo.Echo/Watch",
                                         request_serializer=self.request_type.SerializeToString,
                                         response_deserializer=self.reply_type.FromString)
        replies = list(call(self.request_type(text="demo", count=3), timeout=2))
        self.assertEqual([(item.text, item.sequence) for item in replies], [("demo", 1), ("demo", 2), ("demo", 3)])

    def test_error_and_bounds(self):
        for method, request in (("Fail", self.request_type()), ("Say", self.request_type(count=1001))):
            with self.assertRaises(grpc.RpcError) as failure:
                self.unary(method)(request, timeout=2)
            self.assertEqual(failure.exception.code(), grpc.StatusCode.INVALID_ARGUMENT)

    def test_deadline(self):
        with self.assertRaises(grpc.RpcError) as failure:
            self.unary()(self.request_type(delay_ms=500), timeout=0.02)
        self.assertEqual(failure.exception.code(), grpc.StatusCode.DEADLINE_EXCEEDED)
        self.assertEqual(self.unary()(self.request_type(text="next"), timeout=2).text, "next")

    def test_cancel(self):
        call = self.unary().future(self.request_type(delay_ms=1000), timeout=2)
        self.assertTrue(call.cancel())
        self.assertTrue(call.cancelled())


if __name__ == "__main__":
    unittest.main()
