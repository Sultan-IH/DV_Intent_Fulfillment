import os

import requests as r

MCS_SUB_KEY = os.environ["MCS_SUB_KEY"]
MCS_BASE_URL = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0"


def get_sentiment(text, request_id):
    headers = {
        "Ocp-Apim-Subscription-Key": MCS_SUB_KEY,
        "Content-Type": "application/json"
    }

    json = {
        "documents": [
            {
                "id": request_id,  # looks like a common theme
                "language": "en",
                "text": text
            }
        ]
    }
    resp = r.post(MCS_SUB_KEY + "/sentiment", headers=headers, json=json)

    if resp.status_code != 200:
        raise Exception("MSC returned unexpected status code " + resp.status_code + " expected 200")

    resp = resp.json()
    return resp['documents']
