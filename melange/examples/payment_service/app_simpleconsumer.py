import os

from melange.backends.sqs.elasticmq import LocalSQSBackend
from melange.examples.payment_service.consumer import PaymentConsumer
from melange.examples.payment_service.publisher import PaymentPublisher
from melange.examples.payment_service.repository import PaymentRepository
from melange.examples.payment_service.service import PaymentService
from melange.message_dispatcher import SimpleMessageDispatcher
from melange.publishers import QueuePublisher
from melange.serializers.pickle import PickleSerializer

if __name__ == "__main__":
    serializer = PickleSerializer()
    backend = LocalSQSBackend(
        host=os.environ.get("SQSHOST"), port=os.environ.get("SQSPORT")
    )

    payment_consumer = SimpleMessageDispatcher(
        PaymentConsumer(
            PaymentService(
                PaymentRepository(),
                PaymentPublisher(QueuePublisher(serializer, backend=backend)),
            )
        ),
        PickleSerializer(),
        backend=backend,
    )

    print("Consuming...")
    payment_consumer.consume_loop("payment-updates")
