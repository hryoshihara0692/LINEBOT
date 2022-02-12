import requests
import datetime

API_KEY = '6cdd2bfe5b33d48b1895f2497e83f567'
# openweathermapのエンドポイント(One Call API)
ENDPOINT = 'http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,daily&appid={apikey}&lang=ja'

# # 天気情報を取得する
# # latitude：緯度、longitude：経度
def weather_forecast(latitude, longitude):
    # One Call APIのクエリパラメータを設定
    url = ENDPOINT.format(lat=latitude, lon=longitude, apikey=API_KEY)
    response = requests.get(url)
    response_json = response.json()

    # 現在時刻を取得
    dt = datetime.datetime.now()

    # 現在から2時間後までの天気を取得
    now_hour = str(dt.hour) + "時：" + response_json['hourly'][dt.hour-3]['weather'][0]['description']
    one_hour = str(dt.hour + 1) + "時：" + response_json['hourly'][dt.hour-2]['weather'][0]['description']
    two_hour = str(dt.hour + 2) + "時：" + response_json['hourly'][dt.hour-1]['weather'][0]['description']

    # 言語部分
    chokkin = "送られた場所の天気予報はこんな感じみたいだよ！"
    nl0 = "\n"
    nl1 = "\n\n"

    # return用メッセージを作成
    weather_forecast = chokkin + nl1 + now_hour + nl0 + one_hour + nl0 + two_hour

    return weather_forecast