# ChatGPT 外部実行ツール

このプロジェクトは、Excelデータを基に自動でコンテンツ生成を行い、その結果を再度Excelに保存するシステムです。Microsoft EdgeブラウザとChatGPTを連携させて、指定されたテーマに基づいてコンテンツを生成し、効率的に管理します。

## システム概要

このシステムは、以下の手順で動作します。

1. **Excelからデータを読み込む**: テーマや見出し、エビデンスなどの情報をExcelファイルから取得します。
2. **データの検証**: 読み込んだデータが有効であるか確認し、フラグやエビデンスの有無をチェックします。
3. **コンテンツの生成**: ChatGPTを使って、テーマやエビデンスに基づき、mdファイルやタイトル、ディスクリプション、キーワード、パーマリンクなどのコンテンツを生成します。
4. **結果の保存**: 生成されたコンテンツを再度Excelファイルに保存します。

## 必要なツール

- Python 3.8以上
- Microsoft Edge
- Pip
- Microsoft Edge WebDriver

## Microsoft Edge WebDriverのダウンロード

Microsoft Edgeを自動操作するために、Microsoft Edge WebDriver（`msedgedriver.exe`）が必要です。以下の手順でWebDriverをダウンロードして設定します。

### 手順

1. [Microsoft Edge WebDriverのダウンロードページ](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)にアクセスします。
2. 現在使用しているMicrosoft Edgeのバージョンに一致するWebDriverを選択します。Edgeのバージョンは、Edgeブラウザで `edge://settings/help` にアクセスして確認できます。
3. ダウンロードしたzipファイルを解凍し、`msedgedriver.exe` ファイルを任意のフォルダに配置します。
   - **推奨パス**: `C:\tools\msedgedriver.exe` のように、分かりやすいフォルダに保存します。
4. Pythonスクリプト内で、Edge WebDriverのパスを指定します。

例:

```python
from selenium import webdriver
from selenium.webdriver.edge.service import Service

# msedgedriver.exe のパスを指定
driver_path = "C:/tools/msedgedriver.exe"  # msedgedriverの実際のパスに置き換え
service = Service(driver_path)

# Edge WebDriverを起動
driver = webdriver.Edge(service=service)
```

## 環境変数の設定

このプロジェクトでは、`.env`ファイルを使用して以下の環境変数を設定します。これにより、プログラムの動作に必要な情報を提供します。

| 環境変数名                      | 説明                                                         | 例                                                        |
|---------------------------------|------------------------------------------------------------|----------------------------------------------------------|
| `EXCEL_FILE_PATH`               | Excelファイルのパスを指定します。                                   | `C:\Users\xxx\data\blog.xlsx`                            |
| `WAIT_TIME_AFTER_PROMPT_LONG`   | 長い処理待機時間（秒）を設定します。                                   | `100`                                                    |
| `WAIT_TIME_AFTER_PROMPT_SHORT`  | 短い処理待機時間（秒）を設定します。                                   | `20`                                                     |
| `WAIT_TIME_AFTER_RELOAD`        | ページリロード後の待機時間（秒）を設定します。                             | `10`                                                     |
| `WAIT_TIME_AFTER_SWITCH`        | ウィンドウ切り替え後の待機時間（秒）を設定します。                          | `5`                                                      |
| `SHORT_WAIT_TIME`               | 短い待機時間（秒）を設定します。                                       | `0.8`                                                    |
| `CHATGPT_MODEL_TYPE`            | 使用するChatGPTのモデルタイプを指定します。4oまたは4ominiを指定できます。 | `4omini`                                                 |
| `IS_IMAGE_GENERATION_ENABLED`   | 画像生成を有効にするかどうかを指定します。trueまたはfalseを指定します。     | `true`                                                   |

### `.env`ファイルの例

```plaintext
EXCEL_FILE_PATH=C:\Users\xxx\data\blog.xlsx
WAIT_TIME_AFTER_PROMPT_LONG=100
WAIT_TIME_AFTER_PROMPT_SHORT=30
WAIT_TIME_AFTER_RELOAD=10
WAIT_TIME_AFTER_SWITCH=5
SHORT_WAIT_TIME=0.5
CHATGPT_MODEL_TYPE=4omini
IS_IMAGE_GENERATION_ENABLED=true
```

### モデルタイプと画像生成の設定

このシステムでは、ChatGPTのモデルタイプや画像生成の有効/無効を設定することができます。

- `CHATGPT_MODEL_TYPE`: 使用するChatGPTのモデルタイプを指定します。`4o` または `4omini` から選択し、システムの動作を調整します。
- `IS_IMAGE_GENERATION_ENABLED`: 画像生成を有効にするかを指定します。`true` で画像生成プロセスが有効になります。

## 仮想環境の設定

このプロジェクトを実行する際には、Pythonの仮想環境を使用することを推奨します。これにより、依存するパッケージをプロジェクトごとに管理でき、他のプロジェクトとの衝突を防ぐことができます。

### 仮想環境の作成

1. **仮想環境を作成**:

    ```bash
    python -m venv venv
    ```

2. **仮想環境を有効化**:

    ```bash
    .\venv\Scripts\activate
    ```

3. **必要なパッケージをインストール**:

    ```bash
    pip install -r requirements.txt
    ```

### 仮想環境の終了

仮想環境を終了するには、以下のコマンドを実行します。

```bash
deactivate
```

## 実行方法

1. 仮想環境をアクティブにします。

    ```bash
    .\venv\Scripts\activate
    ```

2. メインスクリプトを実行します。

    ```bash
    python main.py
    ```

これで、Excelファイルに基づいたコンテンツ生成プロジェクトが開始されます。

## `requirements.txt` の更新

新しいパッケージを追加した際には、以下のコマンドで `requirements.txt` を更新します。

```bash
pip freeze > requirements.txt
```

## ログの確認

実行中に発生したエラーや警告は、`logs/execution.log` ファイルで確認できます。
