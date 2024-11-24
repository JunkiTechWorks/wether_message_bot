
# 天気通知Bot

このプロジェクトはPythonを使って天気情報を取得し、LINE Messaging APIを用いてLINEに自動で通知を送るBotです。定期実行やカスタマイズ可能な設定に対応しており、使いやすく拡張性の高い設計になっています。

---

## 概要

- **目的**: 指定した地域（つくば市）の天気予報をLINEで自動通知する。
- **特徴**: 詳細な天気情報（気温、時間別降水確率など）を取得し、メッセージとしてLINEで通知。
- **活用例**: 日々の天気予報確認や業務連絡の自動化に利用可能。

---

## 主な機能

1. **天気情報の取得**
   - 気温、降水確率、風速などの天気データを取得。
   
2. **LINE通知**
   - テキストメッセージやリッチメッセージで天気情報を通知。

3. **定期実行**
   - Pythonの`schedule`ライブラリを用いて毎日決まった時間に通知を送信。

4. **スプレッドシート連携**
   - 取得した天気データをGoogle Sheetsに記録可能。

5. **エラーハンドリング**
   - ネットワークエラーやデータ取得失敗時に適切に対応。

---

## 使用技術

- **プログラミング言語**: Python 3.10.9
- **主要ライブラリ**:
  - `requests`: APIリクエスト
  - `beautifulsoup4`: HTML解析
  - `schedule`: 定期実行
  - `gspread`: Google Sheets連携
  - `dotenv`: 環境変数管理
- **API**:
  - LINE Messaging API

---

## インストール方法

1. **リポジトリをクローン**
   ```bash
   git clone https://github.com/yourusername/weather-line-notifier.git
   cd weather-line-notifier
   ```

2. **必要なライブラリをインストール**
   ```bash
   pip install -r requirements.txt
   ```

3. **環境変数を設定**
   - `.env` ファイルを作成し、以下の情報を記載:
     ```
     LINE_ACCESS_TOKEN=あなたのアクセストークン
     YOUR_USER_ID=送信先のユーザーID
     ```

4. **Google Sheetsの認証情報を設定**（スプレッドシート連携を利用する場合）
   - Google Cloud Platformでサービスアカウントを作成し、`credentials.json`をプロジェクトフォルダに配置。

---

## 使い方

1. **スクリプトを実行**
   ```bash
   python weather_scraper.py
   ```

2. **定期実行を有効化**
   - スクリプトを実行したまま放置するか、タスクスケジューラ（例: crontab）を使用して自動化します。

---

## スケジュール実行

- **Pythonの`schedule`ライブラリ**を使用しています。実行間隔を変更するには、以下のコードを編集してください:
   ```python
   schedule.every().day.at("08:00").do(job)
   ```
   - `08:00`を希望の時間に変更可能。

---

## Google Sheets 設定方法

このプロジェクトではGoogle Sheets APIを使用します。以下の手順に従って設定を行ってください。

1. **Google CloudでAPIを有効化**
   - [Google Cloud Console](https://console.cloud.google.com/)にアクセスします。
   - プロジェクトを作成または選択し、`Google Sheets API`を有効化してください。

2. **サービスアカウントの作成**
   - ナビゲーションメニューから **IAMと管理** > **サービスアカウント** に移動します。
   - 新しいサービスアカウントを作成し、JSON形式でキーをダウンロードしてください。
   - ダウンロードした`credentials.json`をプロジェクトフォルダに配置します。

3. **スプレッドシートの共有**
   - 使用するスプレッドシートを開きます。
   - サービスアカウントのメールアドレスを編集者として共有してください。

4. **環境変数の設定**
   - プロジェクトのルートに`.env`ファイルを作成し、以下を記述します：
     ```
     GOOGLE_APPLICATION_CREDENTIALS=credentials.json
     SPREADSHEET_ID=your_spreadsheet_id
     ```


## 改善のポイント

- **コードの分割**: 機能ごとにクラスや関数を分けて整理。
- **テストケース**: ユニットテストを追加して品質向上。
- **通知内容のカスタマイズ**: ユーザーが表示内容を自由に選べるように。

---

