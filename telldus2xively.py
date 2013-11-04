import oauth2 as oauth
import json, time, requests

XIVELY_API_KEY = ""
XIVELY_FEED_ID = ""

TELLDUS_PUB_KEY = ""
TELLDUS_PRIV_KEY = ""
TELLDUS_TOKEN = ""
TELLDUS_SECRET = ""

XIVELY_URL = "https://api.xively.com/v2/feeds/" + XIVELY_FEED_ID + ".json"
XIVELY_HEADERS = {'content-type': 'application/json', 'X-ApiKey': XIVELY_API_KEY}

consumer = oauth.Consumer(TELLDUS_PUB_KEY, TELLDUS_PRIV_KEY)
token = oauth.Token(TELLDUS_TOKEN, TELLDUS_SECRET)
client = oauth.Client(consumer,token)

while(1):
    try:
        resp, content = client.request('https://api.telldus.com/json/sensors/list?includeValues=1', "GET")
        sensor = json.loads(content)['sensor']
        data = { "version": "1.0.0", "datastreams": [] }
        for s in sensor:
            atTime = time.strftime("%Y-%m-%dT%XZ",time.gmtime(s["lastUpdated"]))
            print s["clientName"]+ "_" + s["name"] + ": " + s["temp"] + " " + s["humidity"] + "%  t: " + str(s["lastUpdated"])
            data["datastreams"].append({ "id": s["clientName"]+ "_" + s["name"] + "_temp",
                                    "datapoints": [{ "at": atTime, "value": s["temp"] }]})
            data["datastreams"].append({ "id": s["clientName"]+ "_" + s["name"] + "_hum",
                                    "datapoints": [{ "at": atTime, "value": s["humidity"] }]})
        r = requests.put(XIVELY_URL, data=json.dumps(data), headers=XIVELY_HEADERS)
        time.sleep(600)
    except (KeyboardInterrupt, SystemExit):
        print
        break
    except:
        time.sleep(600)

