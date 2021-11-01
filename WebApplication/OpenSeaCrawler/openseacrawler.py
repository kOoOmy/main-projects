import requests
import pandas as pd
import json
import base64
from datetime import datetime

headers = {
    "Origin": "https://opensea.io",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://opensea.io/",
    "X-API-KEY": "2f6f419a083c46de9d83ce3dbe7db601",
    "X-BUILD-ID": "gIh7jjVsK1b49tqdzpq1V",
    "Content-Type": "application/json",
    "Connection": "keep-alive"
}

siteurl = "https://api.opensea.io/graphql/"
cursor = "YXJyYXljb25uZWN0aW9uOjk5" #arrayconnection:99
finalcursor = ""
listofdict = []
statdict1 = {}

def makeRequest (request_cursor):
    global finalcursor
    try :
        graphqldata = {"id":"rankingsQuery","query":"query rankingsQuery(\n  $chain: [ChainScalar!]\n  $count: Int!\n  $cursor: String\n  $sortBy: CollectionSort\n  $parents: [CollectionSlug!]\n  $createdAfter: DateTime\n) {\n  ...rankings_collections\n}\n\nfragment rankings_collections on Query {\n  collections(after: $cursor, chains: $chain, first: $count, sortBy: $sortBy, parents: $parents, createdAfter: $createdAfter, sortAscending: false, includeHidden: true, excludeZeroVolume: true) {\n    edges {\n      node {\n        createdDate\n        name\n        slug\n        logo\n        stats {\n          floorPrice\n          marketCap\n          numOwners\n          totalSupply\n          sevenDayChange\n          sevenDayVolume\n          oneDayChange\n          oneDayVolume\n          thirtyDayChange\n          thirtyDayVolume\n          totalVolume\n          id\n        }\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n","variables":{"count":100,"cursor":str(request_cursor),"sortBy":"SEVEN_DAY_VOLUME"}}
        request = requests.post(siteurl, headers=headers, data=json.dumps(graphqldata))
        if request.status_code != 200 or int((request.text.find('errors'))) != -1 :
            print("Status code is not equal to 200 ")
            print("Status code is : ", request.status_code)
            print("Text code is :", request.text)
            raise Exception

        textdata = request.text
        json_dict = json.loads(textdata)
        hasnextpage = json_dict["data"]["collections"]["pageInfo"]["hasNextPage"] # bool
        current_cursor = request_cursor
        cursor_bytes = base64.b64decode(current_cursor)
        base64_cursor = cursor_bytes.decode('ascii')
        location = int(base64_cursor.find(":") + 1)
        nextcursor = str("arrayconnection:" + str(int(base64_cursor[location::]) + int(100)))
        encodedcursor = base64.b64encode(nextcursor.encode('ascii'))
        finalcursor = encodedcursor.decode('ascii')

        for i in range(100):
            statdict = {}
            statdict['name'] = json_dict["data"]["collections"]["edges"][i]["node"]["name"]
            for k, v in json_dict["data"]["collections"]["edges"][i]["node"]["stats"].items():
                statdict[k] = v
            listofdict.append(statdict)

        print(pd.DataFrame(listofdict))


        while hasnextpage:
            makeRequest(finalcursor)
        else:
            raise Exception


    except  :
        df = pd.DataFrame(listofdict)
        print(df)
        df.to_csv(str("opensea"+str(datetime.today().strftime('%H:%M_%d-%m-%y'))+str(".csv")))
        quit()

makeRequest(cursor)

