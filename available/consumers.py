import json
import time
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer

VACCINE_AVAILABILITY_GROUP = "available"


# breakpoint()


class TicksSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })
        print("connected")
        # # Join ticks group
        async_to_sync(self.channel_layer.group_add)(
            VACCINE_AVAILABILITY_GROUP,
            self.channel_name
        )

    def websocket_receive(self, event):
        print("receive")

        i = 0
        while i != 3:
            async_to_sync(self.channel_layer.group_send)(
                VACCINE_AVAILABILITY_GROUP,
                {
                    "type": "new_ticks",
                    "content": json.dumps({"message": "Hello {}".format(i)})
                }
            )
            time.sleep(3)
            i += 1

    def websocket_disconnect(self, event):
        # Leave ticks group
        async_to_sync(self.channel_layer.group_discard)(
            VACCINE_AVAILABILITY_GROUP,
            self.channel_name
        )
        raise StopConsumer()
        print("disconnected")

    def new_ticks(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })
