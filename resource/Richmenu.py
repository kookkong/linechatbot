richdata = {
  "size": {
    "width": 2500,
    "height": 843
  },
  "selected": 'true',
  "name": "Rich Menu 1",
  "chatBarText": "main menu",
  "areas": [
    {
      "bounds": {
        "x": 10,
        "y": 10,
        "width": 823,
        "height": 833
      },
      "action": {
        "type": "message",
        "text": "เช็คราคา"
      }
    },
    {
      "bounds": {
        "x": 843,
        "y": 10,
        "width": 824,
        "height": 833
      },
      "action": {
        "type": "message",
        "text": "เช็คข่าวสาร"
      }
    },
    {
      "bounds": {
        "x": 1686,
        "y": 0,
        "width": 795,
        "height": 843
      },
      "action": {
        "type": "postback",
        "text": "text 3",
        "data": "Data 3"
      }
    }
  ]
}

from app import channel_access_token

import json

import requests

def RegisRich(Rich_json,channel_access_token):

    url = 'https://api.line.me/v2/bot/richmenu'

    Rich_json = json.dumps(Rich_json)

    Authorization = 'Bearer {}'.format(channel_access_token)


    headers = {'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': Authorization}

    response = requests.post(url,headers = headers , data = Rich_json)

    print(str(response.json()['richMenuId']))

    return str(response.json()['richMenuId'])

def CreateRichMenu(ImageFilePath,Rich_json,channel_access_token):

    richId = RegisRich(Rich_json = Rich_json,channel_access_token = channel_access_token)

    url = ' https://api.line.me/v2/bot/richmenu/{}/content'.format(richId)

    Authorization = 'Bearer {}'.format(channel_access_token)

    headers = {'Content-Type': 'image/jpeg',
    'Authorization': Authorization}

    img = open(ImageFilePath,'rb').read()

    response = requests.post(url,headers = headers , data = img)

    print(response.json())


CreateRichMenu(ImageFilePath='Slide1.jpg',Rich_json=richdata,channel_access_token=channel_access_token)