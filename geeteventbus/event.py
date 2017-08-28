''' Event super class '''

import logging
from datetime import datetime


class Event:
    event_type_name = 'Default'

    def __init__(self, topic, event_type_name='Default', ordered=None, event_version=None):
        self.topic = topic
        self.event_version = event_version
        self.ordered = ordered
        self.occurred_on = datetime.now()
        self.event_type_name = event_type_name

        if self.ordered is not None:
            if type(self.ordered) is not str:
                logging.error('Invalid type' + type(self.ordered))
                raise ValueError('Ordered field must be a string')

    def get_topic(self):
        '''
        Returns the topic associated with the topic

        :returns: the topic of the event
        :rtype: str
        '''
        return self.topic

    def get_ordered(self):
        '''
        Returns the event ordering field.

        Event ordering field may be none, specifying the events may get processed out of order
        
        :returns: the ordering field of the event object
        :rtype: str
        '''
        return self.ordered

    def get_event_version(self):
        return self.event_version

    def get_occurred_on(self):
        return self.occurred_on

    @classmethod
    def get_event_type_name(cls):
        return cls.event_type_name
