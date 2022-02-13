from importlib.resources import contents
from flask import Flask, request, abort
from linebot import (
    LineBotApi
    , WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent
    , PostbackEvent
    , TextMessage
    , TextSendMessage
    , TemplateSendMessage
    , LocationMessage
    , FlexSendMessage
    , ButtonsTemplate
    , PostbackAction
)
import os, dotenv
import weather_forecast as wf

app = Flask(__name__)
 
# 環境変数取得
# LINE Developers: アクセストークン/ChannelSecret
dotenv.load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
 
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
 
# Webhookからのリクエストの署名検証部分
@app.route("/callback", methods=['POST'])
def callback():
    # 署名検証のための値
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # 署名検証
    try:
        handler.handle(body, signature)
    except InvalidSignatureError: # 失敗したとき エラー
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 以降で ボット処理内容について記載 =========================================

# メッセージイベント
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # オウム返し処理
    # text_sent_by_user = event.message.text
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=text_sent_by_user))

    # # ダイアログ形式処理
    # user_id = "U0a1a79622789287ae8d94df0f3a67d71"
    # buttons_template_message = TemplateSendMessage(
    #     alt_text='Buttons template',
    #     template=ButtonsTemplate(
    #         title='Menu',
    #         text='Please select',
    #         actions=[
    #             PostbackAction(
    #                 label='postback',
    #                 display_text='postback text',
    #                 data='action=buy&itemid=1'
    #             )
    #         ]
    #     )
    # )
    # line_bot_api.push_message(user_id, buttons_template_message)

    # 受信メッセージを区別
    user_message = event.message.text
    # 区別メッセージ
    today_weather = "きょうの天気は？"
    # 返信用メッセージ
    gps_link = "https://line.me/R/nv/location/"
    default_message = "いまは天気を教えてあげることしかできないんだ…"
    gps_request_message = "↑のリンクを押して天気を知りたい場所を教えて！\n(検索せずに送信すると現在地の天気が分かるよ！)"

    if user_message == today_weather:
        # 現在地を催促する処理 → 位置情報イベントへ
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(gps_link + "\n" + gps_request_message))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(default_message))

# # ポストバックイベント
# @handler.add(PostbackEvent)
# def on_postback(line_event):
#     data = line_event.postback.data
#     line_bot_api.reply_message(line_event.reply_token, TextSendMessage("reply to postback text"))

# 位置情報イベント
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(line_event):
    # 緯度経度を取得
    user_lat = line_event.message.latitude
    user_lon = line_event.message.longitude
    # 天気予報を取得
    flex_message_wf = wf.weather_forecast(user_lat, user_lon)
    # 天気予報を返信
    line_bot_api.reply_message(
        line_event.reply_token, FlexSendMessage(
            alt_text='alt_text',
            # contentsにdict型の値を渡す
            contents=flex_message_wf
        ))
# ====================================================================

# python main.py　で動作
if __name__ == "__main__":
    app.run(port=5000)