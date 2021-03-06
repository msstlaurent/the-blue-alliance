import json

from helpers.event_manipulator import EventManipulator
from helpers.memcache.memcache_webcast_flusher import MemcacheWebcastFlusher


class EventWebcastAdder(object):

    @classmethod
    def add_webcast(cls, event, webcast):
        """Takes a webcast dictionary and adds it to an event"""

        if event.webcast:
            webcasts = event.webcast
            if webcast in webcasts:
                return event
            else:
                webcasts.append(webcast)
                event.webcast_json = json.dumps(webcasts)
        else:
            event.webcast_json = json.dumps([webcast])
        event.dirty = True
        EventManipulator.createOrUpdate(event)
        MemcacheWebcastFlusher.flushEvent(event.key_name)

        return event
