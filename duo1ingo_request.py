import os
import requests
import json
import time
from itertools import product

my_user_id = os.environ['user_id']
my_auth = os.environ['Authorization']
my_user_list = my_user_id.split(",")
my_auth_list = my_auth.split(",")

id_lists = ["general_xp_boost", "xp_boost_60", "streak_freeze","society_streak_freeze", "health_refill"]


def make_request():
    url = "https://android-api-cf.duolingo.com/2017-06-30/batch?fields=responses%7Bbody%2Cstatus%2Cheaders%7D"
    for id in id_lists:
        for auth, user in zip(my_auth_list, my_user_list):
            headers = {
                "Cookie": "wuuid=b91f4ddf-d4f4-4ef8-b47c-04f5531e85db",
                "Authorization": f"Bearer {auth}",
                "User-Agent": "Duodroid/5.128.3 Dalvik/2.1.0 (Linux; U; Android 13; RMX3360 Build/TQ3C.230901.001.B1)",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip, deflate",
            }

            request_data = {
                "requests": [{
                    "body": rf'{{"id": "{id}", "isFree": true, "consumed": true}}',
                    "bodyContentType": "application/json",
                    "method": "POST",
                    "url": rf"/2017-06-30/users/{user}/shop-items?fields=id%2CpurchaseDate%2CpurchasePrice%2Cquantity%2CsubscriptionInfo%7Bcurrency%2CexpectedExpiration%2CisFreeTrialPeriod%2CperiodLength%2Cprice%2CproductId%2Crenewer%2Crenewing%2CvendorPurchaseId%7D%2CwagerDay%2CexpectedExpirationDate%2CpurchaseId%2CremainingEffectDurationInSeconds%2CexpirationEpochTime%2CfamilyPlanInfo%7BownerId%2CsecondaryMembers%2CinviteToken%2CpendingInvites%7BfromUserId%2CtoUserId%2Cstatus%7D%7D",
                }],
                "includeHeaders":
                False,
            }

            try:
              request_data_json = json.dumps(request_data)
              response = requests.post(url, data=request_data_json, headers=headers)
              response.raise_for_status()
              with open("response_output.json", 'w') as output_file:
               json.dump(response.json(), output_file, indent=2)
              print("Successfully bought" + " " + id + " for " + user)
            except requests.exceptions.RequestException as ex:
              print(f"Request error: {ex}")


    time.sleep(60)


make_request()
