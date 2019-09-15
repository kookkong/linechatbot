import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
#แก้เป็น *
from linebot.models import *

app = Flask(__name__)
#แก้้ Secret กับ Token
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', '306a9b647f7a3940c495a611795e5d5b')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN','Ts53mybWj36sOab2Nkaf1e8GIR84fXs9oGACww83n0/wPkhic0kcJtquvDSB4xTMkqYR41+eiR5vb/1IL2qmh1J8R2aZMRBk84feTeMgYbavyQ+yqjlKOsYZ7ntb9jPp2nm+pDB3zO2gLsAgqs3xMAdB04t89/1O/w1cDnyilFU=')
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    ### Function reply token
    #line_bot_api.reply_message(
        #event.reply_token, #ได้ reply token
        #TextSendMessage(text=event.message.text)) #ส่ง Token
    Reply_token = event.reply_token
    text_fromUser = event.message.text ## ข้อความจาก user
    #text_tosend_1 = TextMessage(text='Uncle engineer',quick_reply=None)
    #text_tosend_2 = TextMessage(text='Uncle engineer - 02',quick_reply=None)

    #image_message_1 = ImageSendMessage(
        #original_content_url= 'https://storage.thaipost.net/main/uploads/photos/big/20190125/image_big_5c4a707dad998.jpg'
        #,preview_image_url='https://storage.thaipost.net/main/uploads/photos/big/20190125/image_big_5c4a707dad998.jpg'
    #)

    if 'เช็คราคา' in text_fromUser:
        from resource.bxAPI import GetBxPrice
        from random import randint
        num = randint(1,10)
        data = GetBxPrice(Number_to_get=num) ## เก็บจำนวนข้อมูล
        
        from resource.FlexMessage import setCarousel, setbubble

        flex = setCarousel(data)

        from resource.reply import SetMenuMessage_Object, send_flex

        flex = SetMenuMessage_Object(flex)
        send_flex(Reply_token,file_data = flex,bot_access_key=channel_access_token)
    else:
        text_list = [
                "I don't know what are you talking about",
                'ขออภัยครับ'
                'ขอโทษครับ'
                'กรุณาลองใหม่อีกครั้ง'
        ]
        from random import choice
        text_data = choice(text_list)
        text = TextSendMessage(text=text_data)
        line_bot_api.reply_message(Reply_token,text)

@handler.add(FollowEvent)
def RegisRichmenu(event):
    userid = event.source.user_id
    disname = line_bot_api.get_profile(user_id=userid).display_name
    button_1 = QuickReplyButton(action=MessageAction(label='เช็คราคา',text='เช็คราคา'))
    button_2 = QuickReplyButton(action=MessageAction(label='เช็คข่าวสาร',text='เช็คข่าวสาร'))
    qbtn = QuickReply(items=[button_1,button_2])

    text = TextSendMessage(text='สวัสดีคุณ {} ยินดีต้อนรับสู่บริการแชทบอท'.format(disname))
    text_2 = TextSendMessage(text='กรุณาเลือกเมนู่ที่ต้องการ',quick_reply= qbtn)

    line_bot_api.link_rich_menu_to_user(userid,'richmenu-6be5931f8c9609f8493982244208c520')

    line_bot_api.reply_message(event.reply_token,messages=[text,text_2])


        #text_tosend = TextSendMessage(text=str(price))
        #line_bot_api.reply_message(Reply_token,text_tosend)

    #line_bot_api.reply_message(
        #Reply_token,
        #messages = [text_tosend_1,text_tosend_2,image_message_1]
           
    
if __name__ == "__main__":
    app.run(port=8888)