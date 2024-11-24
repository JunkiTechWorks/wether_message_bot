import requests
from bs4 import BeautifulSoup
import schedule
import time
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import Optional, List

# === 設定 ===
load_dotenv()
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
YOUR_USER_ID = os.getenv("YOUR_USER_ID")
SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = "1Vf3QNSn6NIGrL6Nuy-SWfVjP2xQQ8Obw7V2rTMCGItU"
SHEET_NAME = "シート1"
WEATHER_URL = "https://tenki.jp/forecast/3/11/4020/8220/"

# Google Sheets APIの認証設定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)
worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# === 関数 ===
def send_line_message(message: str) -> None:
    """
    LINEにメッセージを送信する。
    :param message: 送信するメッセージ内容
    """
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

def record_weather_to_sheet(data: List[str]) -> None:
    """
    天気データをGoogleスプレッドシートに記録する。
    :param data: 記録するデータ（リスト形式）
    """
    try:
        today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([today_date] + data)
        print("スプレッドシートに記録しました。")
    except Exception as e:
        print(f"スプレッドシート記録エラー: {e}")

def fetch_weather_data(url: str) -> Optional[str]:
    """
    天気データを取得し、LINEメッセージ形式で返す。
    :param url: 天気情報のURL
    :return: メッセージ内容またはNone（取得失敗時）
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 天気データ取得
        today_high_temp = soup.find('section', class_='today-weather').find('dd', class_='high-temp temp').find('span', 'value').text
        today_low_temp = soup.find('section', class_='today-weather').find('dd', class_='low-temp temp').find('span', 'value').text
        today_weather = soup.find('section', class_='today-weather').find('p', 'weather-telop').text
        rain_prob_row = soup.find('tr', class_='rain-probability')
        rain_probs = [td.text for td in rain_prob_row.find_all('td')]

        # スプレッドシート用データ
        sheet_data = [today_high_temp, today_low_temp, today_weather] + rain_probs
        record_weather_to_sheet(sheet_data)

        # LINEメッセージ作成
        rain_probabilities = "\n".join([f"{i*6}時: {prob}" for i, prob in enumerate(rain_probs)])
        return (f"今日の天気予報:\n"
                f"最高気温: {today_high_temp}度\n"
                f"最低気温: {today_low_temp}度\n"
                f"天気: {today_weather}\n"
                f"降水確率:\n{rain_probabilities}")
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")
        return None
    except AttributeError:
        print("天気情報を取得できませんでした。HTML構造を確認してください。")
        return None

def job() -> None:
    """
    定期実行タスク。
    天気データを取得し、LINE通知を送信。
    """
    weather_message = fetch_weather_data(WEATHER_URL)
    if weather_message:
        send_line_message(weather_message)

# === メイン処理 ===
if __name__ == "__main__":
    # スケジュール設定
    schedule.every().day.at("07:00").do(job)  # 毎朝7時に実行
    print("スケジュールされたタスクを実行中...")
    
    # 定期実行ループ
    while True:
        schedule.run_pending()
        time.sleep(1)