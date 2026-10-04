"""Serve the committed descriptor using public generic gRPC handlers."""

import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import grpc
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

SCHEMA = Path(__file__).resolve().parent / "schema/echo.pb"


def messages():
    files = descriptor_pb2.FileDescriptorSet.FromString(SCHEMA.read_bytes())
    pool = descriptor_pool.DescriptorPool()
    for entry in files.file:
        pool.Add(entry)
    return tuple(message_factory.GetMessageClass(pool.FindMessageTypeByName(name)) for name in (
        "archverity.demo.EchoRequest", "archverity.demo.EchoReply", "google.protobuf.Empty",
    ))


def make_server(port=18429):
    request_type, reply_type, empty_type = messages()

    def validate(request, context):
        if len(request.text.encode("utf-8")) > 32768 or not 0 <= request.count <= 1000 or not 0 <= request.delay_ms <= 5000:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "demo bounds exceeded")

    def wait(request, context):
        end = time.monotonic() + request.delay_ms / 1000
        while time.monotonic() < end:
            if not context.is_active():
                return False
            time.sleep(min(0.02, max(0, end - time.monotonic())))
        return context.is_active()

    def say(request, context):
        validate(request, context)
        if not wait(request, context):
            context.abort(grpc.StatusCode.CANCELLED, "demo cancelled")
        return reply_type(text=request.text, sequence=1)

    def watch(request, context):
        validate(request, context)
        for sequence in range(1, (request.count or 3) + 1):
            if not wait(request, context):
                return
            yield reply_type(text=request.text, sequence=sequence)

    def fail(_request, context):
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "intentional demo failure")

    def unary(callback, input_type=request_type):
        return grpc.unary_unary_rpc_method_handler(callback, request_deserializer=input_type.FromString,
                                                  response_serializer=reply_type.SerializeToString)

    executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="demo-grpc")
    server = grpc.server(executor, maximum_concurrent_rpcs=4, options=[
        ("grpc.max_receive_message_length", 65536), ("grpc.max_send_message_length", 65536),
    ])
    server.add_generic_rpc_handlers((grpc.method_handlers_generic_handler("archverity.demo.Echo", {
        "Health": unary(lambda _request, _context: reply_type(text="ok", sequence=1), empty_type),
        "Say": unary(say), "Fail": unary(fail),
        "Watch": grpc.unary_stream_rpc_method_handler(watch, request_deserializer=request_type.FromString,
                                                      response_serializer=reply_type.SerializeToString),
    }),))
    bound_port = server.add_insecure_port(f"127.0.0.1:{port}")
    if not bound_port:
        executor.shutdown(wait=True)
        raise OSError(f"Cannot bind gRPC port {port}")
    return server, executor, bound_port
