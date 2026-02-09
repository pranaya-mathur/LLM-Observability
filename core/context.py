import contextvars
from uuid import uuid4

request_id_ctx = contextvars.ContextVar("request_id")
trace_id_ctx = contextvars.ContextVar("trace_id")

def init_context():
    req = uuid4()
    trace = uuid4()
    request_id_ctx.set(req)
    trace_id_ctx.set(trace)
    return req, trace
