# ChatGPT 外部実行ツール

このプロジェクトは、Excelデータを元に自動でコンテンツ生成を行い、その結果をExcelに保存するためのシステムです。Microsoft EdgeブラウザとChatGPTを連携させて、指定されたテーマに基づいてプロンプトを送信し、得られたコンテンツを適切に管理します。

## システム概要

このシステムは以下の手順で動作します:

1. **Excelからデータを読み込む**: Excelファイルから指定された列のデータを取得します。これには、テーマ、見出し、エビデンスなどの情報が含まれます。

2. **データの検証**: 読み込んだデータが有効であるかどうかを検証します。フラグやエビデンスの有無を確認します。

3. **コンテンツの生成**: ChatGPTを使用して、テーマやエビデンスに基づいたコンテンツ（mdファイル、タイトル、ディスクリプション、キーワード、パーマリンク）を生成します。

4. **結果の保存**: 生成されたコンテンツを再度Excelファイルに保存します。

## 必要なツール

- Python 3.8以上
- Microsoft Edge
- Pip

## 環境変数の設定

このプロジェクトでは、`.env`ファイルを使用して以下の環境変数を設定します。これにより、プログラムの動作に必要な情報が提供されます。

| 環境変数名                     | 説明                                                                | 例                                                       |
|-----------------------------|-------------------------------------------------------------------|---------------------------------------------------------|
| `EXCEL_FILE_PATH`            | Excelファイルのパスを指定します。                                           | `C:\Users\xxx\data\blog.xlsx`                           |
| `WAIT_TIME_AFTER_PROMPT_LONG`  | 長い処理待機時間（秒）を設定します。                                        | `100`                                                   |
| `WAIT_TIME_AFTER_PROMPT_SHORT` | 短い処理待機時間（秒）を設定します。                                        | `20`                                                    |
| `WAIT_TIME_AFTER_RELOAD`      | ページリロード後の待機時間（秒）を設定します。                                    | `10`                                                    |
| `WAIT_TIME_AFTER_SWITCH`      | ウィンドウ切り替え後の待機時間（秒）を設定します。                                 | `5`                                                     |
| `SHORT_WAIT_TIME`             | 短い待機時間（秒）を設定します。                                             | `0.8`                                                   |
| `TITLE_PROMPT`                | タイトル生成のためのプロンプトを指定します。                                     | `"上記のタイトルを考えて。下記のキーワードを入れて\n---\n{}"` |
| `PERMALINK_PROMPT`            | パーマリンク生成のためのプロンプトを指定します。                                   | `"パーマリンクを考えて"`                                    |
| `LONG_DESCRIPTION_PROMPT`     | 長いディスクリプション生成のためのプロンプトを指定します。                          | `"上記のメタディスクリプションを長めに考えて"`                    |
| `SHORT_DESCRIPTION_PROMPT`    | 短いディスクリプション生成のためのプロンプトを指定します。                          | `"もう少し短くして"`                                      |
| `KEYWORDS_PROMPT`             | キーワード生成のためのプロンプトを指定します。                                   | `"上記のメタキーワードを考えてください。,で区切って書いてください。"` |
| `IMAGE_PROMPT`                | 画像生成のためのプロンプトを指定します。                                       | `"記事に合う横長の画像を作ってください。"`                          |
| `CHATGPT_MODEL_TYPE`          | 使用するChatGPTのモデルタイプを指定します。4oまたは4ominiを指定できます。           | `4omini`                                                |
| `IS_IMAGE_GENERATION_ENABLED` | 画像生成を有効にするかどうかを指定します。trueまたはfalseを指定します。               | `true`                                                  |

### `.env`ファイルの例

```plaintext
EXCEL_FILE_PATH=C:\Users\okubo\OneDrive\ドキュメント\004_blogs\succulent\data\blog.xlsx
WAIT_TIME_AFTER_PROMPT_LONG=100
WAIT_TIME_AFTER_PROMPT_SHORT=30
WAIT_TIME_AFTER_RELOAD=10
WAIT_TIME_AFTER_SWITCH=5
SHORT_WAIT_TIME=0.5
TITLE_PROMPT="上記のタイトルを考えて。下記のキーワードを入れて\n---\n{}"
PERMALINK_PROMPT="パーマリンクを考えて"
LONG_DESCRIPTION_PROMPT="上記のメタディスクリプションを長めに考えて"
SHORT_DESCRIPTION_PROMPT="もう少し短くして"
KEYWORDS_PROMPT="上記のメタキーワードを考えてください。,で区切って書いてください。"
IMAGE_PROMPT="記事に合う横長の画像を作ってください。"
CHATGPT_MODEL_TYPE=4omini
IS_IMAGE_GENERATION_ENABLED=true
```

### モデルタイプと画像生成の設定

このシステムでは、使用するChatGPTモデルタイプや画像生成の有効化を設定することができます。

- `CHATGPT_MODEL_TYPE` には、使用するChatGPTのモデルタイプを指定します。`4o` または `4omini` のどちらかを指定することで、システムの動作を適切に調整します。特定の機能（例: キー操作の繰り返し回数など）がモデルタイプによって異なる場合があります。

- `IS_IMAGE_GENERATION_ENABLED` は、画像生成を有効にするかどうかを制御するフラグです。`true` に設定すると、記事に関連する画像を生成するプロンプトが自動的に送信されます。`false` に設定すると、画像生成のプロセスはスキップされます。

## 仮想環境の設定

このプロジェクトを実行する前に、Pythonの仮想環境を設定することをお勧めします。これにより、依存パッケージをプロジェクトごとに管理し、他のプロジェクトとの衝突を防ぐことができます。

### 仮想環境作成

もし仮想環境に問題がある場合は、以下の手順で仮想環境を削除し、再作成してください。

1. **新しい仮想環境を作成**:

    ```bash
    python -m venv venv
    ```

2. **仮想環境をアクティブにする**:

    ```bash
    .\venv\Scripts\activate
    ```

3. **必要なパッケージをインストールする**:

    ```bash
    pip install -r requirements.txt
    ```

### 仮想環境の終了

仮想環境の使用を終了するには、以下のコマンドを実行します。

```bash
deactivate
```

### 仮想環境の再作成

1. **仮想環境の削除**:

    スタートメニューを開き、"PowerShell" と入力します。
    "Windows PowerShell" を右クリックし、「管理者として実行」を選択します。

    ```powershell
    Remove-Item -Recurse -Force venv
    ```

    もしくはエクスプローラーから`venv`を削除します。

2. **仮想環境を作成**:

    [仮想環境作成](#仮想環境作成)の手順を実施します。

## 実行方法（作成済の場合はこちらから）

1. 仮想環境をアクティブにします。

    ```bash
    .\venv\Scripts\activate
    ```

2. メインスクリプトを実行します。

    ```bash
    python main.py
    ```

これで、プロジェクトが開始され、Excelファイルに基づいてコンテンツが生成されます。

## requirements.txt を更新

```bash
pip freeze > requirements.txt
```

## ログの確認

実行中に発生したエラーや警告を確認するには、`logs/execution.log`ファイルを参照してください。
