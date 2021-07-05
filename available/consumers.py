import requests
import datetime
import json
import time
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from find_availability import AvailableSlots

VACCINE_AVAILABILITY_GROUP = "available_slots"


# breakpoint()

class SlotsSyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })
        print("connected")
        # # Join ticks group

    async def websocket_receive(self, event):
        print("receive")
        self.today = datetime.datetime.now().date()
        self.dates = ['-'.join(str(self.today + datetime.timedelta(days=i)).split('-')[::-1]) for i in range(1, 8)]
        self.district_id = event.get('text', None)
        while True:
            for date in self.dates:
                list_of_dicts = sync_to_async(self.slot_data)(date)
                for x in await list_of_dicts:
                    if x['min_age_limit'] == 45 and x['available_capacity'] > 0:
                        # and x['fee_type']!='Paid':
                        await self.send(
                            {
                                "type": "websocket.send",
                                "text": json.dumps(x)
                            }
                        )
                time.sleep(3)

    async def websocket_disconnect(self, event):
        # Leave ticks group
        raise StopConsumer()
        print("disconnected")

    def slots(self, event):
        print("slots function")
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })

    def slot_data(self, date):
        self.URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
        headers = {
            "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "accept-language": 'en-US,en;q=0.9',
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
        }
        PARAMS = {
            'district_id': self.district_id,
            'date': date
        }
        r = self.response(self.URL, PARAMS, headers)
        list_of_dicts = json.loads(r.content.decode())['sessions']
        return list_of_dicts

    def response(self, URL, PARAMS, headers):
        self.resp = requests.get(url=URL, params=PARAMS, headers=headers)
        if self.resp.status_code != 200:
            time.sleep(30)
            print("waiting........")
            self.response(URL, PARAMS, headers)
        return self.resp
