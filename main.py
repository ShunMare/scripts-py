import os
import pandas as pd
from dotenv import load_dotenv
from handlers.excel_handler import ExcelHandler
from handlers.edge_handler import EdgeHandler
from handlers.keyboard_handler import KeyboardHandler
from handlers.chatgpt_handler import ChatGPTHandler
from generators.prompt_generator import PromptGenerator
from utils.data_retriever import (
    get_flag,
    get_theme,
    get_heading,
    get_evidences,
    check_flag_and_evidences,
)
from generators.content_generator import ContentGenerator

load_dotenv()

# 定数の設定
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH")
WAIT_TIME_AFTER_PROMPT_LONG = int(os.getenv("WAIT_TIME_AFTER_PROMPT_LONG", 20))
WAIT_TIME_AFTER_PROMPT_SHORT = int(os.getenv("WAIT_TIME_AFTER_PROMPT_SHORT", 5))
WAIT_TIME_AFTER_RELOAD = int(os.getenv("WAIT_TIME_AFTER_RELOAD", 5))
SHORT_WAIT_TIME = float(os.getenv("SHORT_WAIT_TIME", 0.5))
GROUP_SIZE = 10
CHATGPT_MODEL_TYPE = os.getenv("CHATGPT_MODEL_TYPE", "4o")
IS_IMAGE_GENERATION_ENABLED = (
    os.getenv("IS_IMAGE_GENERATION_ENABLED", "false").lower() == "true"
)

# 各種ハンドラーのインスタンスを作成
excel_handler = ExcelHandler(EXCEL_FILE_PATH)
edge_handler = EdgeHandler(wait_time_after_switch=WAIT_TIME_AFTER_RELOAD)
keyboard_handler = KeyboardHandler(short_wait_time=SHORT_WAIT_TIME)
chatgpt_handler = ChatGPTHandler(
    short_wait_time=SHORT_WAIT_TIME, model_type=CHATGPT_MODEL_TYPE
)
prompt_generator = PromptGenerator(
    keyboard_handler,
    chatgpt_handler,
    WAIT_TIME_AFTER_PROMPT_SHORT,
    WAIT_TIME_AFTER_PROMPT_LONG,
)
content_generator = ContentGenerator(
    edge_handler,
    keyboard_handler,
    chatgpt_handler,
    prompt_generator,
    WAIT_TIME_AFTER_RELOAD,
    WAIT_TIME_AFTER_PROMPT_SHORT,
    WAIT_TIME_AFTER_PROMPT_LONG,
)

# Excelファイルを読み込み、列情報を事前に取得
wb, ws = excel_handler.load_excel()
if not wb or not ws:
    print("Failed to load Excel workbook.")
    exit()

# 各列のインデックスを取得
column_indices = {
    "flag": excel_handler.find_matching_index(1, "flag", is_row_flag=True),
    "md": excel_handler.find_matching_index(1, "md", is_row_flag=True),
    "title": excel_handler.find_matching_index(1, "title", is_row_flag=True),
    "description": excel_handler.find_matching_index(
        1, "description", is_row_flag=True
    ),
    "link": excel_handler.find_matching_index(1, "link", is_row_flag=True),
    "keywords": excel_handler.find_matching_index(1, "keywords", is_row_flag=True),
    "theme": excel_handler.find_matching_index(1, "theme", is_row_flag=True),
    "heading": excel_handler.find_matching_index(1, "heading", is_row_flag=True),
    "evidence": excel_handler.find_matching_index(1, "evidence", is_row_flag=True),
}


# データ処理関数
def generate_and_process_prompts(group, start_row, column_indices):
    """指定されたグループのプロンプトを生成し、処理する"""
    first_row = int(group.index[0]) + 2

    flag = get_flag(excel_handler, first_row, column_indices)
    theme = get_theme(excel_handler, first_row, column_indices)
    heading = get_heading(excel_handler, first_row, column_indices)
    evidences = get_evidences(excel_handler, column_indices, group)

    if not check_flag_and_evidences(flag, evidences, first_row):
        return

    # 各種コンテンツの生成
    md_content = content_generator.get_md(theme, heading, evidences)
    title_content = content_generator.get_title(theme)  # themeを渡す
    content_generator.send_prompt_and_generate_content(
        os.getenv("LONG_DESCRIPTION_PROMPT"), 0
    )
    description_content = content_generator.get_description()
    keywords_content = content_generator.get_keywords()
    permalink_content = content_generator.get_permalink()
    if IS_IMAGE_GENERATION_ENABLED:
        content_generator.send_prompt_and_generate_content(os.getenv("IMAGE_PROMPT"), 0)

    # Excelに保存する処理
    flag_row = start_row + 2
    success = excel_handler.update_cells(
        target_index=flag_row,
        target_indices=[
            column_indices["md"],
            column_indices["title"],
            column_indices["description"],
            column_indices["keywords"],
            column_indices["link"],
        ],
        values=[
            md_content,
            title_content,
            description_content,
            keywords_content,
            permalink_content,
        ],
        row_flag=True,
    )

    if success:
        excel_handler.save_to_excel()


# グループごとに処理を実行
grouped = pd.read_excel(EXCEL_FILE_PATH).groupby(lambda idx: idx // GROUP_SIZE)

for i, (_, group) in enumerate(grouped):
    start_row = i * GROUP_SIZE
    print(f"\nProcessing group starting at row {start_row}")
    generate_and_process_prompts(group, start_row, column_indices)

print("\nAll prompts have been processed and results saved to Excel.")
