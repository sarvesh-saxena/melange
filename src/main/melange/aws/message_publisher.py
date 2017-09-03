import logging

from melange.event import Event
from melange.aws.messaging_manager import MessagingManager


class MessagePublisher:
    def __init__(self, event_serializer, topic):
        self.topic = MessagingManager.declare_topic(topic)
        self.event_serializer = event_serializer

    def publish(self, event):

        if not isinstance(event, Event):
            logging.error('Invalid data passed. You must pass an event instance')
            return False

        response = self.topic.publish(Message=self.event_serializer.serialize(event))

        if 'MessageId' not in response:
            raise ConnectionError('Could not send the event to the SNS TOPIC')

        return True
