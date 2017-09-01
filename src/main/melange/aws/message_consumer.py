import json
import logging
from queue import Empty

from melange.aws.messaging_manager import MessagingManager
from melange.subscriber import Subscriber


class MessageConsumer:
    def __init__(self, event_serializer, event_queue_name, topic_to_subscribe):

        super().__init__()

        self.event_serializer = event_serializer
        self.consumers = {}
        topic = MessagingManager.declare_topic(topic_to_subscribe)
        self.event_queue, _ = MessagingManager.declare_queue(event_queue_name, topic)

    def subscribe(self, consumer):

        if not isinstance(consumer, Subscriber):
            return False

        listened_event_type_name = consumer.listens_to()

        if listened_event_type_name not in self.consumers:
            self.consumers[listened_event_type_name] = []

        self.consumers[listened_event_type_name].append(consumer)

        return True

    def unsubscribe(self, consumer):

        listened_event_type_name = consumer.listens_to()

        if listened_event_type_name in self.consumers and consumer in self.consumers[listened_event_type_name]:
            self.consumers[listened_event_type_name].remove(consumer)

            if len(self.consumers[listened_event_type_name]) == 0:
                del self.consumers[listened_event_type_name]

    def consume_event(self):

        eventobj = self._get_next_event()
        if eventobj is not None:
            self._process_event(eventobj)

    def _get_subscribers(self, event_type_name):
        return self.consumers[event_type_name] if event_type_name in self.consumers else []

    def _get_next_event(self):

        messages = self.event_queue.receive_messages(MaxNumberOfMessages=1, VisibilityTimeout=100,
                                                     WaitTimeSeconds=10)

        try:
            for message in messages:
                body = message.body
                message.delete()
                message_content = json.loads(body)

                if 'Message' in message_content:
                    content = json.loads(message_content['Message'])
                else:
                    content = message_content

                if 'event_type_name' in content:
                    return self.event_serializer.deserialize(content)
                else:
                    raise Exception("No event_type_name")

        except Empty:
            return None
        except Exception as e:
            logging.error(e)
            return None

    def _process_event(self, eventobj):
        for subscr in self._get_subscribers(eventobj.event_type_name):

            try:
                subscr.process(eventobj)
            except Exception as e:
                logging.error(e)
