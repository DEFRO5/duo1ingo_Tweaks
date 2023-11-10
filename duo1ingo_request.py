import os
import requests
import json
import time

my_user_id = os.environ['user_id']
my_auth = os.environ['Authorization']
my_user_list = my_user_id.split(",")
my_auth_list = my_auth.split(",")

id_lists = ["xp_boost_stackable", "unlimited_hearts_boost", "society_streak_freeze", "streak_freeeze", "health_refill", ]

def make_request(auth_indx=0, user_indx=0, id_indx=0):
    if auth_indx == len(my_auth_list):
        auth_indx = 0  # Reset auth index value
        user_indx = 0  # Reset user index value
        id_indx += 1 

    if id_indx == len(id_lists):
        return  # Move to next id

    auth = my_auth_list[auth_indx]
    user = my_user_list[user_indx]
    id = id_lists[id_indx]

    url = "https://android-api-cf.duolingo.com/2017-06-30/batch?fields=responses%7Bbody%2Cstatus%2Cheaders%7D"

    headers = {
        "Cookie": "wuuid=b91f4ddf-d4f4-4ef8-b47c-04f5531e85db",
        "Authorization": rf"Bearer {auth}",
        "User-Agent": "Duodroid/5.117.4 Dalvik/2.1.0 (Linux; U; Android 13; RMX3360 Build/TQ3C.230901.001.B1)",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate",
    }

    request_data = {
        "requests": [
            {
                "body": rf'{{"id": "{id}", "isFree": true, "consumed": true}}',
                "bodyContentType": "application/json",
                "method": "POST",
                "url": rf"/2017-06-30/users/{user}/shop-items?fields=id%2CpurchaseDate%2CpurchasePrice%2Cquantity%2CsubscriptionInfo%7Bcurrency%2CexpectedExpiration%2CisFreeTrialPeriod%2CperiodLength%2Cprice%2CproductId%2Crenewer%2Crenewing%2CvendorPurchaseId%7D%2CwagerDay%2CexpectedExpirationDate%2CpurchaseId%2CremainingEffectDurationInSeconds%2CexpirationEpochTime%2CfamilyPlanInfo%7BownerId%2CsecondaryMembers%2CinviteToken%2CpendingInvites%7BfromUserId%2CtoUserId%2Cstatus%7D%7D",
            }
        ],
        "includeHeaders": False,
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
    auth_indx, user_indx = auth_indx + 1, user_indx + 1
    make_request(auth_indx, user_indx, id_indx) # Recursive

# Start the recursive function with all indices starting from 0
make_request()
time.sleep(120)
