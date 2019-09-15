from flask import Flask, request
import pprint
from wolf import search_wiki

app = Flask(__name__)
access_token = 'Ts53mybWj36sOab2Nkaf1e8GIR84fXs9oGACww83n0/wPkhic0kcJtquvDSB4xTMkqYR41+eiR5vb/1IL2qmh1J8R2aZMRBk84feTeMgYbavyQ+yqjlKOsYZ7ntb9jPp2nm+pDB3zO2gLsAgqs3xMAdB04t89/1O/w1cDnyilFU='
@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':

        pp = pprint.PrettyPrinter(indent=3)
        #dictionary from line
        data = request.json
        data_show = pp.pprint(data)
        print(data_show)

        text_fromline = data['events'][0]['message']['text']
        result = search_wiki(text_fromline)

        print(result)

        from reply import ReplyMessage

        ReplyMessage(Reply_token=data['events'][0]['replyToken'],
        TextMessage=result,
        Line_Access_Token = access_token
        )

        return 'OK'

    elif request.method == 'GET':
        return 'this is web page for recieving package'

if __name__ == "__main__":
    app.run(port=8888)