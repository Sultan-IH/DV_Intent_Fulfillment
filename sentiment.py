import os

import requests as r

MCS_SUB_KEY = "e66fc899750542d4b1fd1e0ae7063a82"
MCS_BASE_URL = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0"
counter = 1

def get_sentiment(text, request_id):
    print("get sent for ", text, " id: ", request_id)
    global counter

    headers = {
        "Ocp-Apim-Subscription-Key": MCS_SUB_KEY,
        "Content-Type": "application/json"
    }

    json = {
        "documents": [
            {
                "id": counter,  # looks like a common theme
                "language": "en",
                "text": text
            }
        ]
    }
    resp = r.post(MCS_BASE_URL + "/sentiment", headers=headers, json=json)

    if resp.status_code != 200:
        print(resp.json())
        raise Exception("MSC returned unexpected status code " + str(resp.status_code) + " expected 200")

    counter += 1
    resp = resp.json()
    return resp['documents'][0]
