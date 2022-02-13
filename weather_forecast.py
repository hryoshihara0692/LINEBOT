import requests
import datetime
import json

API_KEY = '6cdd2bfe5b33d48b1895f2497e83f567'
# openweathermapのエンドポイント(One Call API)
ENDPOINT = 'http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,daily&appid={apikey}&lang=ja'

# # 天気情報を取得する
# # latitude：緯度、longitude：経度
def weather_forecast(latitude, longitude):
    # One Call APIのクエリパラメータを設定
    url = ENDPOINT.format(lat=latitude, lon=longitude, apikey=API_KEY)
    response = requests.get(url)
    weather_forecast_json = response.json()

    # 現在時刻を取得
    dt = datetime.datetime.now()

    # 現在～3時間後のテキスト作成
    now_hour = str(dt.hour-3) + "時(現在)"
    one_hour = str(dt.hour-2) + "時"
    two_hour = str(dt.hour-1) + "時"
    three_hour = str(dt.hour) + "時"

    # (要)21～3時ころのUTC時刻とのズレ対策
    # 現在から2時間後までの天気を取得
    now_hour_wf = weather_forecast_json['hourly'][dt.hour-3]['weather'][0]['description']
    one_hour_wf = weather_forecast_json['hourly'][dt.hour-2]['weather'][0]['description']
    two_hour_wf = weather_forecast_json['hourly'][dt.hour-1]['weather'][0]['description']
    three_hour_wf = weather_forecast_json['hourly'][dt.hour]['weather'][0]['description']

    # きょうの天気予報 --- UTC時刻取得のため、hourly + 3時間が取得対象時間
    early_morning_wf   = weather_forecast_json['hourly'][3]['weather'][0]['description']
    morning_wf         = weather_forecast_json['hourly'][6]['weather'][0]['description']
    noon_wf            = weather_forecast_json['hourly'][9]['weather'][0]['description']
    afternoon_wf       = weather_forecast_json['hourly'][12]['weather'][0]['description']
    early_evening_wf   = weather_forecast_json['hourly'][15]['weather'][0]['description']
    night_wf           = weather_forecast_json['hourly'][18]['weather'][0]['description']

    # flex_massege.json読み込み
    with open('flex_message_wf.json', 'r', encoding="UTF-8") as f:
        flex_message_wf_json = json.load(f)
    
    # Jsonの値更新（直近の天気）
    # 現在時刻
    flex_message_wf_json['body']['contents'][4]['contents'][1]['contents'][0]['text'] = now_hour
    # 現在の天気
    flex_message_wf_json['body']['contents'][4]['contents'][1]['contents'][1]['text'] = now_hour_wf
    # 1時間後の時刻
    flex_message_wf_json['body']['contents'][4]['contents'][2]['contents'][0]['text'] = one_hour
    # 1時間後の天気
    flex_message_wf_json['body']['contents'][4]['contents'][2]['contents'][1]['text'] = one_hour_wf
    # 2時間後の時刻
    flex_message_wf_json['body']['contents'][4]['contents'][3]['contents'][0]['text'] = two_hour
    # 2時間後の天気
    flex_message_wf_json['body']['contents'][4]['contents'][3]['contents'][1]['text'] = two_hour_wf
    # 3時間後の時刻
    flex_message_wf_json['body']['contents'][4]['contents'][4]['contents'][0]['text'] = three_hour
    # 3時間後の天気
    flex_message_wf_json['body']['contents'][4]['contents'][4]['contents'][1]['text'] = three_hour_wf

    # Jsonの値更新（一日の天気）
    # 朝の天気
    flex_message_wf_json['body']['contents'][4]['contents'][7]['contents'][1]['text'] = early_morning_wf
    # 午前の天気
    flex_message_wf_json['body']['contents'][4]['contents'][8]['contents'][1]['text'] = morning_wf
    # 昼の天気
    flex_message_wf_json['body']['contents'][4]['contents'][9]['contents'][1]['text'] = noon_wf
    # 午後の天気
    flex_message_wf_json['body']['contents'][4]['contents'][10]['contents'][1]['text'] = afternoon_wf
    # 夕方の天気
    flex_message_wf_json['body']['contents'][4]['contents'][11]['contents'][1]['text'] = early_evening_wf
    # 夜の天気
    flex_message_wf_json['body']['contents'][4]['contents'][12]['contents'][1]['text'] = night_wf

    return flex_message_wf_json