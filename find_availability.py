# importing the requests library
import requests
import datetime
import pprint
import json
import time
from scripts.async_functions import get_or_create_event_loop, send_to_room


class AvailableSlots:

    def __init__(self, district):
        # api-endpoint
        self.URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
        self.district = district
        # 678: Moradabad, 651: ghaziabad, 503: Kota

        self.district_id = self.district if self.district else 651
        self.today = datetime.datetime.now().date()
        self.dates = ['-'.join(str(self.today + datetime.timedelta(days=i)).split('-')[::-1]) for i in range(1, 8)]
        # print(self.dates)
        import os

        count = 0

    def response(self, URL, PARAMS, headers):
        self.resp = requests.get(url=URL, params=PARAMS, headers=headers)
        if self.resp.status_code != 200:
            time.sleep(30)
            print("waiting........")
            self.response(URL, PARAMS, headers)
        return self.resp

    def results(self):
        while (True):
            for date in self.dates:
                PARAMS = {
                    'district_id': self.district_id,
                    'date': date
                }

                headers = {
                    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    "accept-language": 'en-US,en;q=0.9',
                    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
                }

                # sending get request and saving the response as response object
                r = self.response(self.URL, PARAMS, headers)

                # count += 1
                # if count == 100:
                #     os.system("ipconfig /renew")
                #     count = 0
                # extracting data in json format
                list_of_dicts = json.loads(r.content.decode())['sessions']
                # open(file=)
                for x in list_of_dicts:
                    if x['min_age_limit'] == 45 and x['available_capacity'] > 0:
                            # and x['fee_type'] != 'Paid':
                        print((
                            date,
                            'fee_type : ' + x['fee_type'],
                            'Available doses : ' + str(x['available_capacity']),
                            x['name'],
                            x['address'] + ', Pin_Code : ' + str(x['pincode']),
                        ))
                time.sleep(3)
            #     print("---------------------------- Internal For end ----------------------------")
            # print("---------------------------- outer For end ----------------------------")
            # print("-------------------------- while repeat -----------------------------")
