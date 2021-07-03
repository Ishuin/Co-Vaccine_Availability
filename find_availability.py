# importing the requests library
import requests
import datetime
import pprint
import json
import time

# api-endpoint
URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"

# 678: Moradabad, 651: ghaziabad, 503: Kota

district_id = 651
today = datetime.datetime.now().date()
dates = ['-'.join(str(today + datetime.timedelta(days=i)).split('-')[::-1]) for i in range(1, 8)]
print(dates)
import os

count = 0


def response(URL, PARAMS, headers):
    r = requests.get(url=URL, params=PARAMS, headers=headers)
    if r.status_code != 200:
        time.sleep(30)
        print("waiting........")
        response(URL, PARAMS, headers)
    return r


while (True):
    for date in dates:
        PARAMS = {
            'district_id': district_id,
            'date': date
        }

        headers = {
            "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "accept-language": 'en-US,en;q=0.9',
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
        }

        # sending get request and saving the response as response object
        r = response(URL, PARAMS, headers)

        # count += 1
        # if count == 100:
        #     os.system("ipconfig /renew")
        #     count = 0
        # extracting data in json format
        list_of_dicts = json.loads(r.content.decode())['sessions']
        # open(file=)
        for x in list_of_dicts:
            if x['min_age_limit'] == 18 and x['available_capacity'] > 0 and x['fee_type']!='Paid':
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
