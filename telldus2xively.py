import oauth2 as oauth
import json, time, requests

XIVELY_API_KEY = "dhaFNLu_mglOIqdwx7uPRy476zWSAKxtbW1jOHZjcFdiWT0g"
XIVELY_FEED_ID = "temp"

TELLDUS_PUB_KEY = "FEHUVEW84RAFR5SP22RABURUPHAFRUNU"
TELLDUS_PRIV_KEY = "ZUXEVEGA9USTAZEWRETHAQUBUR69U6EF"
TELLDUS_TOKEN = "7e9c78c7dc6304a4e622041a6b0e5265052850283"
TELLDUS_SECRET = "d3984696f87035517aab9b61524a3327"

XIVELY_URL = "https://api.xively.com/v2/feeds/" + XIVELY_FEED_ID + ".json"
XIVELY_HEADERS = {'content-type': 'application/json', 'X-ApiKey': XIVELY_API_KEY}

consumer = oauth.Consumer(TELLDUS_PUB_KEY, TELLDUS_PRIV_KEY)
token = oauth.Token(TELLDUS_TOKEN, TELLDUS_SECRET)
client = oauth.Client(consumer,token)

while(1):
    try:
        resp, content = client.request('https://api.telldus.com/json/sensors/list?includeValues=1', "GET")
        sensor = json.loads(content)['inne']
        data = { "version": "1.0.0", "datastreams": [] }
        for s in sensor:
            atTime = time.strftime("%Y-%m-%dT%XZ",time.gmtime(s["lastUpdated"]))
            print s["clientName"]+ "_" + s["name"] + ": " + s["temp"] + " " + "%  t: " + str(s["lastUpdated"])
            data["datastreams"].append({ "id": s["clientName"]+ "_" + s["name"] + "_temp",
                                    "datapoints": [{ "at": atTime, "value": s["temp"] }]})
      
        r = requests.put(XIVELY_URL, data=json.dumps(data), headers=XIVELY_HEADERS)
        time.sleep(600)
    except (KeyboardInterrupt, SystemExit):
        print
        break
    except:
        time.sleep(600)

