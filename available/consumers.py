import requests
import datetime
import json
import time
from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

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
        scope_headers = {x[0].decode("utf-8"):x[1].decode("utf-8") for x in self.scope['headers']}
        today = datetime.datetime.now().date()
        dates = ['-'.join(str(today + datetime.timedelta(days=i)).split('-')[::-1]) for i in range(1, 8)]
        district_id = event.get('text', None)
        while True:
            for date in dates:
                time.sleep(3)
                list_of_dicts = sync_to_async(self.slot_data)(date, district_id, scope_headers)
                dicts = await list_of_dicts
                await self.send(
                    {
                        "type": "websocket.send",
                        "text": json.dumps({"date":date})
                    }
                )
                for x in dicts:
                    if x['min_age_limit'] == 45 and x['available_capacity'] > 0:
                        # and x['fee_type']!='Paid':
                        await self.send(
                            {
                                "type": "websocket.send",
                                "text": json.dumps(x)
                            }
                        )

    async def websocket_disconnect(self, event):
        # Leave ticks group
        print("disconnected")
        raise StopConsumer()

    def slots(self, event):
        print("slots function")
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })

    def slot_data(self, date, district_id, scope_headers):
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
        headers = {
            "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
            + 'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "accept-language": scope_headers['accept-language'],
            "user-agent": scope_headers['user-agent'],
        }
        params = {
            'district_id': district_id,
            'date': date
        }
        r = self.response(url, params, headers)
        list_of_dicts = json.loads(r.content.decode())['sessions']
        return list_of_dicts

    def response(self, url, params, headers):
        resp = requests.get(url=url, params=params, headers=headers)
        if resp.status_code != 200:
            time.sleep(30)
            print("waiting........")
            self.response(url, params, headers)
        return resp
