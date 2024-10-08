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
| `SHORT_WAIT_TIME`               | 短い待機時間（秒）を設定します。                                       | `0.5`                                                    |
| `CHATGPT_MODEL_TYPE`            | 使用するChatGPTのモデルタイプを指定します。                            | `4o`                                                 |
| `IS_IMAGE_GENERATION_ENABLED`   | 画像生成を有効にするかどうかを指定します。                               | `false`                                                   |
| `CHATGPT_URL`                   | ChatGPTのURLを指定します。                                       | `https://chatgpt.com/`                                   |
| `PROMPT_TEMPLATE_PATH`          | プロンプトテンプレートファイルのパスを指定します。                          | `C:\Users\xxx\scripts\chatgpt\prompt\initial_prompt_template.txt` |
| `TITLE_PROMPT`                  | タイトル生成用のプロンプトを指定します。                                | `"上記のタイトルを考えて。下記のキーワードを入れて\n---\n{}"`              |
| `LONG_DESCRIPTION_PROMPT`       | 長い説明文生成用のプロンプトを指定します。                              | `"上記のメタディスクリプションを長めに考えて"`                          |
| `SHORT_DESCRIPTION_PROMPT`      | 短い説明文生成用のプロンプトを指定します。                              | `"もう少し短くして"`                                           |
| `KEYWORDS_PROMPT`               | キーワード生成用のプロンプトを指定します。                              | `"上記のメタキーワードを考えてください。,で区切って書いてください。"`      |
| `PERMALINK_PROMPT`              | パーマリンク生成用のプロンプトを指定します。                            | `"パーマリンクを考えて"`                                        |
| `IMAGE_PROMPT`                  | 画像生成用のプロンプトを指定します。                                  | `"記事に合う横長の画像を作ってください。"`                            |
| `THUMBNAIL_IMAGE_PROMPT`                  | 画像生成用のプロンプトを指定します。                                  | `"記事のサムネの背景画像を横長で作ってください。その上に文字を乗せるので、そんなに派手じゃない方が見やすいかも。"`                            |
| `BING_URL`                      | BingのURLを指定します。                                         | `https://www.bing.com/chat?form=NTPCHB`                   |
| `HEADING_PROMPT`                | 見出し生成用のプロンプトを指定します。                                | `"下記の見出しを参考にブログの記事のH2、H3の見出しを考えて\n１つにまとめて書いて、それ以外出力しないで\nSNS関連の見出しは不要です\n全体の流れを意識してh2とh3を構造的に書いてください"` |

### `.env`ファイルの例

```plaintext
# common
WAIT_TIME_AFTER_PROMPT_LONG=100
WAIT_TIME_AFTER_PROMPT_MEDIUM=100
WAIT_TIME_AFTER_PROMPT_SHORT=5
WAIT_TIME_AFTER_RELOAD=5
WAIT_TIME_AFTER_SWITCH=3
SHORT_WAIT_TIME=0.5
DOWNLOAD_FOLDER_PATH=C:\Users\name\Downloads\
SCRIPT_BASE_DIR=C:\Users\name\OneDrive\ドキュメント\004_blogs\succulent\scripts\
GET_CONTENT_METHOD=html
EXECUTE_CREATE_BLOG_WP=true
EXECUTE_CREATE_BLOG_MD=false

# **Create blog wp related variables**
SCRIPT_CREATE_BLOG_WP_DIR=C:\Users\name\OneDrive\ドキュメント\004_blogs\succulent\scripts\create_blog_wp\
EXECUTE_GET_THEMES_GOOGLE=true
EXECUTE_GET_HEADING_GOOGLE=true
EXECUTE_GET_DIRECTION=false
EXECUTE_GET_EVIDENCE_BING=false
EXECUTE_CREATE_BLOG_WP_CHATGPT=true
EXECUTE_UPLOAD_WP_POST=true
CREATE_BLOG_WP_EXCEL_FILE_PATH=C:\Users\name\OneDrive\ドキュメント\004_blogs\succulent\data\blog_wp.xlsx
CREATE_BLOG_WP_EXCEL_GROUP_SIZE=10
CREATE_BLOG_WP_EXCEL_INDEX_ROW=1
CREATE_BLOG_WP_EXCEL_START_ROW=2
DIRECTION_REMOVE_TEXT="SNS"

# **Create blog md related variables**
SCRIPT_CREATE_BLOG_MD_DIR=C:\Users\name\OneDrive\ドキュメント\004_blogs\succulent\scripts\create_blog_md\
CREATE_BLOG_MD_FOLDER_PATH=C:\Users\name\OneDrive\ドキュメント\004_blogs\succulent\scripts\create_blog_md\
CREATE_BLOG_MD_EXCEL_FILE_PATH=C:\Users\name\OneDrive\ドキュメント\004_blogs\succulent\data\blog_md.xlsx
CREATE_BLOG_MD_EXCEL_INDEX_ROW=1
CREATE_BLOG_MD_EXCEL_START_ROW=2
CREATE_BLOG_MD_TARGET_FOLDER_PATH=C:\Users\name\OneDrive\デスクトップ\vba\
CREATE_BLOG_MD_TARGET_MDX_FILE_NAME=index.mdx
CREATE_BLOG_MD_TARGET_PNG_FILE_NAME=featured.png
CREATE_BLOG_MD_MOVE_TO_DESTINATION_FOLDER_PATH=C:\Users\okubo\OneDrive\ドキュメント\001_repositories\nexunity\src\content\posts\

EXECUTE_CREATE_BLOG_MD_CHATGPT=true
EXECUTE_CREATE_FOLDER_AND_FILE=false
EXECUTE_CREATE_BLOG_CHATGPT=false
EXECUTE_GET_TITLE_IN_MD=true
EXECUTE_REPLACE_TEXT=false
EXECUTE_CREATE_THUMBNAIL=true
EXECUTE_MOVE_TARGET_FOLDERS=false
EXECUTE_DELETE_FILES_IN_FOLDERS=false

CREATE_PNG_FONTS_DIR_NAME=fonts
CREATE_PNG_SETTINGS_DIR_NAME=settings
CREATE_PNG_IMAGES_DIR_NAME=images
CREATE_PNG_TAG_NAME="CSS"
CREATE_PNG_CONFIG_NAME=CSS
TARGET_FOLDER_PREFIX=css-

# chatgpt
CHATGPT_MODEL_TYPE=gpts
IS_IMAGE_GENERATION_ENABLED=false
CHATGPT_URL=https://chatgpt.com/
# CHATGPT_URL=https://chatgpt.com/?model=o1-mini
# CHATGPT_URL=https://chatgpt.com/g/g-7d2cNjZ3E-tech-blog-master
PROMPT_TEMPLATE_PATH=C:\Users\name\OneDrive\ドキュメント\004_blogs\succulent\scripts\create_blog_wp\prompt\initial_prompt_template.txt
TITLE_PROMPT="上記のタイトルを考えて。下記のキーワードを入れて\n---\n{theme}\n\nタイトルだけを「」などつけずに書いて"
LONG_DESCRIPTION_PROMPT="上記のメタディスクリプションを長めに考えて"
SHORT_DESCRIPTION_PROMPT="もう少し短くして、メタディスクリプションのみ出力して、他は書かないで。"
KEYWORDS_PROMPT="上記のメタキーワードを考えてください。,で区切って書いてください。メタキーワードのみ出力して、他は書かないで。"
PERMALINK_PROMPT="パーマリンクを考えて\n---\nただし、先頭に'/'はつけないで、シンプルにcorpuscularia-lehmanniiのように出力して"
IMAGE_PROMPT="記事に合う横長の画像を作ってください。"
THUMBNAIL_IMAGE_PROMPT="記事のサムネの背景画像を横長で作ってください。その上に文字を乗せるので、そんなに派手じゃない方が見やすいかも。"
CHATGPT_OUTPUT_ELEMENT="div"
CHATGPT_OUTPUT_CLASS_LIST="markdown,prose"
CHATGPT_TMP_FILE_NAME="create_blog_chatgpt"
SOURCE_COPILOT_CONVERSATION="ソース: Copilot との会話"
SUPERSCRIPT_CITATION_PATTERN=\s*[⁰¹²³⁴⁵⁶⁷⁸⁹]+:\s*\[[^\]]+\]\([^\)]+\)

# bing
BING_URL=https://www.bing.com/chat?form=NTPCHB
BING_OUTPUT_ELEMENT="div"
BING_OUTPUT_CLASS_LIST="content,user-select-text"
BING_TMP_FILE_NAME="get_evidence_bing"

# google
HEADING_PROMPT="下記の見出しを参考にブログの記事のH2、H3の見出しを考えて\n１つにまとめて書いて、それ以外出力しないで\nSNS関連の見出しは不要です\n全体の流れを意識してh2とh3を構造的に書いてください。h2やh3とわざわざ書かないで。リストでインデントだけ行って。先頭に数字を記載しないで。"
DIRECTION_PROMPT="{theme}について下記の内容で詳しく情報をください。\n"

# wp
WP_URL=https://aaa.blog
WP_USERNAME=aaa@gmail.com
WP_APP_PASSWORD="xxx ccc vvv eee oooo ppppp"
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
    python -m scripts.create_blog
    ```

これで、Excelファイルに基づいたコンテンツ生成プロジェクトが開始されます。

## `requirements.txt` の更新

新しいパッケージを追加した際には、以下のコマンドで `requirements.txt` を更新します。

```bash
pip freeze > requirements.txt
```

## ログの確認

実行中に発生したエラーや警告は、`logs/execution.log` ファイルで確認できます。
