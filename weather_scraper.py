import requests
from bs4 import BeautifulSoup
import schedule
import time
import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数から値を取得
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
YOUR_USER_ID = os.getenv("YOUR_USER_ID")

# 確認用（実際の運用時は削除）
print(f"LINE_ACCESS_TOKEN: {LINE_ACCESS_TOKEN}")
print(f"YOUR_USER_ID: {YOUR_USER_ID}")


def send_line_message(message):
    """LINEにメッセージを送信する"""
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": YOUR_USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("LINEメッセージを送信しました。")
    except requests.exceptions.RequestException as e:
        print(f"LINEメッセージ送信エラー: {e}")

def fetch_weather_data(url):
    """天気データを取得する"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        today_high_temp = soup.find('section', class_='today-weather').find('dd', class_='high-temp temp').find('span', class_='value').text
        today_low_temp = soup.find('section', class_='today-weather').find('dd', class_='low-temp temp').find('span', class_='value').text
        today_weather = soup.find('section', class_='today-weather').find('p', class_='weather-telop').text

        return f"今日の天気予報:\n最高気温: {today_high_temp}度\n最低気温: {today_low_temp}度\n天気: {today_weather}"
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")
        return None
    except AttributeError:
        print("天気情報を取得できませんでした。HTML構造を確認してください。")
        return None

def job():
    """定期実行タスク"""
    url = "https://tenki.jp/forecast/3/11/4020/8220/"
    weather_message = fetch_weather_data(url)
    if weather_message:
        send_line_message(weather_message)

# スケジュール設定
schedule.every().day.at("13:39").do(job)  # 毎朝8時に実行

print("スケジュールされたタスクを実行中...")

# 定期実行のループ
while True:
    schedule.run_pending()
    time.sleep(1)
