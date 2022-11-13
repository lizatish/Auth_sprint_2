from flask import current_app
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configure_tracer() -> None:
    resource = Resource(attributes={
        "service.name": current_app.config['AUTH_SERVICE_NAME']
    })
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=current_app.config['JAEGER_HOSTNAME'],
                agent_port=current_app.config['JAEGER_PORT'],
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
