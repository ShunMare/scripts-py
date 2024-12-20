# ブログ生成 外部実行ツール

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

## 環境変数の設定

このプロジェクトでは、`.env`ファイルを使用して以下の環境変数を設定します。これにより、プログラムの動作に必要な情報を提供します。

| 環境変数名                      | 説明                                                         | 例                                                        |
|---------------------------------|------------------------------------------------------------|----------------------------------------------------------|
| `EXCEL_FILE_PATH`               | Excelファイルのパスを指定します。                                   | `C:\Users\xxx\data\blog.xlsx` |
| `WAIT_TIME_AFTER_PROMPT_LONG`   | 長い処理待機時間（秒）を設定します。                                   | `200`                                                    |
| `WAIT_TIME_AFTER_PROMPT_SHORT`  | 短い処理待機時間（秒）を設定します。                                   | `100`                                                     |
| `WAIT_TIME_AFTER_RELOAD`        | ページリロード後の待機時間（秒）を設定します。                             | `5`                                                     |
| `WAIT_TIME_AFTER_SWITCH`        | ウィンドウ切り替え後の待機時間（秒）を設定します。                          | `3`                                                      |
| `KEYBOARD_ACTION_SHORT_DELAY`               | 短い待機時間（秒）を設定します。                                       | `0.5`                                                    |
| `CREATE_BLOG_WP_CHATGPT_MODEL_TYPE`            | 使用するChatGPTのモデルタイプを指定します。                            | `4o`                                                 |
| `CREATE_BLOG_WP_IS_IMAGE_GENERATION_ENABLED`   | 画像生成を有効にするかどうかを指定します。                               | `false`                                                   |
| `CHATGPT_URL`                   | ChatGPTのURLを指定します。                                       | `https://chatgpt.com/`                                   |
| `CREATE_BLOG_WP_PROMPT_TEMPLATE_FULL_PATH`          | プロンプトテンプレートファイルのパスを指定します。                          | `C:\Users\xxx\scripts\chatgpt\prompt\initial_prompt_template.txt` |
| `CREATE_BLOG_WP_TITLE_PROMPT`                  | タイトル生成用のプロンプトを指定します。                                | `"上記のタイトルを考えて。下記のキーワードを入れて\n---\n{}"`              |
| `CREATE_BLOG_WP_LONG_DESCRIPTION_PROMPT`       | 長い説明文生成用のプロンプトを指定します。                              | `"上記のメタディスクリプションを長めに考えて"`                          |
| `CREATE_BLOG_WP_SHORT_DESCRIPTION_PROMPT`      | 短い説明文生成用のプロンプトを指定します。                              | `"もう少し短くして"`                                           |
| `CREATE_BLOG_WP_KEYWORDS_PROMPT`               | キーワード生成用のプロンプトを指定します。                              | `"上記のメタキーワードを考えてください。,で区切って書いてください。"`      |
| `CREATE_BLOG_WP_PERMALINK_PROMPT`              | パーマリンク生成用のプロンプトを指定します。                            | `"パーマリンクを考えて"`                                        |
| `CREATE_BLOG_WP_IMAGE_PROMPT`                  | 画像生成用のプロンプトを指定します。                                  | `"記事に合う横長の画像を作ってください。"`                            |
| `CREATE_BLOG_WP_THUMBNAIL_IMAGE_PROMPT`                  | 画像生成用のプロンプトを指定します。                                  | `"記事のサムネの背景画像を横長で作ってください。その上に文字を乗せるので、そんなに派手じゃない方が見やすいかも。"`                            |
| `BING_URL`                      | BingのURLを指定します。                                         | `https://www.bing.com/chat?form=NTPCHB`                   |
| `CREATE_BLOG_WP_HEADING_PROMPT`                | 見出し生成用のプロンプトを指定します。                                | `"下記の見出しを参考にブログの記事のH2、H3の見出しを考えて\n１つにまとめて書いて、それ以外出力しないで\nSNS関連の見出しは不要です\n全体の流れを意識してh2とh3を構造的に書いてください"` |

### `.env`ファイルの例

`.env.example`を参照。

### モデルタイプと画像生成の設定

このシステムでは、ChatGPTのモデルタイプや画像生成の有効/無効を設定することができます。

- `CREATE_BLOG_WP_CHATGPT_MODEL_TYPE`: 使用するChatGPTのモデルタイプを指定します。`4o` または `4omini` から選択し、システムの動作を調整します。
- `CREATE_BLOG_WP_IS_IMAGE_GENERATION_ENABLED`: 画像生成を有効にするかを指定します。`true` で画像生成プロセスが有効になります。

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
    .\scripts\venv\Scripts\activate
    ```

2. メインスクリプトを実行します。

    ```bash
    python -m scripts.create_content
    ```

これで、Excelファイルに基づいたコンテンツ生成プロジェクトが開始されます。

## `requirements.txt` の更新

新しいパッケージを追加した際には、以下のコマンドで `requirements.txt` を更新します。

```bash
pip freeze > requirements.txt
```

## ログの確認

実行中に発生したエラーや警告は、`logs/execution.log` ファイルで確認できます。

## Google Sheets API 認証情報の取得手順

1. credentials.json の取得:

   a. Google Cloud Console (<https://console.cloud.google.com/>) にアクセスします。
   b. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
   c. 左側のメニューから「APIとサービス」→「ライブラリ」を選択します。
   d. 検索バーで "Google Sheets API" を検索し、有効にします。
   e. 「認証情報を作成」をクリックします。
   f. 「どの API を使用していますか?」で "Google Sheets API" を選択します。
   g. 「どこから API を呼び出しますか?」で "その他の UI (Windows、CLI ツールなど)" を選択します。
   h. 「アクセスするデータの種類は?」で "ユーザーデータ" を選択します。
   i. 「次へ」をクリックし、OAuth クライアント ID を作成します。
   j. アプリケーション名を入力し、必要に応じて他の詳細を設定します。
   k. 「作成」をクリックします。
   l. 認証情報ページで、作成した OAuth 2.0 クライアント ID の横にある下向き矢印をクリックし、「JSONをダウンロード」を選択します。
   m. ダウンロードしたJSONファイルの名前を `credentials.json` に変更し、スクリプトと同じディレクトリに配置します。

2. token.json の生成:

   a. `token.json` は、スクリプトを初めて実行したときに自動的に生成されます。
   b. スクリプトを実行すると、ブラウザが開き、Google アカウントでの認証が求められます。
   c. 認証が成功すると、`token.json` ファイルがスクリプトのディレクトリに自動的に作成されます。

3. 環境変数の設定:

   credentials.json と token.json のパスを環境変数として設定します。

   Unix/Linux/macOS の場合:

   ```
   export GOOGLE_CREDENTIALS_PATH=/path/to/your/credentials.json
   export GOOGLE_TOKEN_PATH=/path/to/your/token.json
   ```

   Windows の場合:

   ```
   set GOOGLE_CREDENTIALS_PATH=C:\path\to\your\credentials.json
   set GOOGLE_TOKEN_PATH=C:\path\to\your\token.json
   ```

   または、スクリプト内で直接パスを指定することもできます。

注意:

- `credentials.json` には機密情報が含まれているため、安全に保管し、公開リポジトリにアップロードしないように注意してください。
- `token.json` は自動生成されますが、これも機密情報を含むため、安全に保管してください。
- 環境変数を使用する場合、スクリプトを実行する前に毎回設定する必要があります。永続的に設定したい場合は、システムの環境変数設定を使用するか、.env ファイルなどの設定ファイルを利用することを検討してください。

## Google Sheets API の料金体系

1. 無料枠:
   - Google Sheets API は Google Cloud Platform の無料枠に含まれています。
   - 1日あたり500リクエストまでは無料で利用可能です。

2. 無料枠を超えた場合:
   - 500リクエスト/日を超えると、$1.50 USD / 100,000リクエストの料金が発生します。

3. クォータと制限:
   - デフォルトのクォータ: 1分あたり300リクエスト、1日あたり60,000リクエスト。
   - これらの制限は、Google Cloud Console で調整可能です（場合によっては追加料金が発生する可能性があります）。

4. 注意点:
   - 個人プロジェクトや小規模な使用であれば、無料枠内で十分に収まる可能性が高いです。
   - 大規模なデータ処理や頻繁なAPI呼び出しを行う場合は、料金が発生する可能性があります。
   - Google Cloud Platformでは、予期せぬ高額請求を防ぐために予算アラートを設定することができます。

5. コスト管理:
   - Google Cloud Console で使用量とコストを監視できます。
   - 予算アラートを設定し、一定の使用量に達した場合に通知を受け取ることができます。

6. その他の考慮事項:
   - Google Workspace（旧G Suite）ユーザーの場合、追加の特典や異なる制限が適用される場合があります。
   - エンタープライズ向けの追加サポートやサービスレベルアグリーメント（SLA）が必要な場合は、別途料金が発生します。

結論:
通常の個人使用や小規模なプロジェクトであれば、Google Sheets API は実質的に無料で利用できる可能性が高いです。ただし、大規模な使用や高頻度のAPI呼び出しを行う場合は、コストが発生する可能性があるため、使用量を慎重に監視し、必要に応じて予算管理を行うことが重要です。

## prompt hints

```plaintext
cot
メタ認知を利用して
水平思考　斬新
スキャッパー法を使って
a to zで考えて
```
