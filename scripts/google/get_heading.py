import os
import sys
import logging
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
sys.path.append(project_root)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 環境変数を取得し、デフォルト値を設定
load_dotenv(dotenv_path, override=True)
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "")
WAIT_TIME_AFTER_PROMPT_LONG = int(os.getenv("WAIT_TIME_AFTER_PROMPT_LONG", 200))
WAIT_TIME_AFTER_PROMPT_SHORT = int(os.getenv("WAIT_TIME_AFTER_PROMPT_SHORT", 100))
WAIT_TIME_AFTER_RELOAD = int(os.getenv("WAIT_TIME_AFTER_RELOAD", 5))
WAIT_TIME_AFTER_SWITCH = int(os.getenv("WAIT_TIME_AFTER_SWITCH", 3))
SHORT_WAIT_TIME = float(os.getenv("SHORT_WAIT_TIME", 0.5))
EDGE_DRIVER_PATH = os.getenv("EDGE_DRIVER_PATH", "")
CHATGPT_PATH = os.getenv("CHATGPT_PATH", "https://chatgpt.com/")
CHATGPT_MODEL_TYPE = os.getenv("CHATGPT_MODEL_TYPE", "4o")
HEADING_PROMPT = os.getenv("HEADING_PROMPT", "")
GROUP_SIZE = 10

import pandas as pd
from handlers.excel_handler import ExcelHandler
from handlers.edge_handler import EdgeHandler
from handlers.keyboard_handler import KeyboardHandler
from generators.prompt_generator import PromptGenerator
from utils.data_retriever import (
    get_flag,
    get_theme,
    check_flag_and_theme,
)
from analyzers.google_search_analyzer import GoogleSearchAnalyzer
from handlers.json_processor import JSONProcessor
from utils.formatter import Formatter
from generators.chatgpt_content_generator import ChatGPTContentGenerator
from handlers.chatgpt_handler import ChatGPTHandler
from handlers.text_processor import TextProcessor

# 各種ハンドラーのインスタンスを作成
excel_handler = ExcelHandler(EXCEL_FILE_PATH)
google_analyzer = GoogleSearchAnalyzer()
text_processor = TextProcessor()
edge_handler = EdgeHandler(
    driver_path=EDGE_DRIVER_PATH,
    wait_time_after_switch=WAIT_TIME_AFTER_SWITCH,
)
keyboard_handler = KeyboardHandler(short_wait_time=SHORT_WAIT_TIME)
chatgpt_handler = ChatGPTHandler(
    edge_handler=edge_handler,
    keyboard_handler=keyboard_handler,
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
    model_type=CHATGPT_MODEL_TYPE,
)
prompt_generator = PromptGenerator(
    keyboard_handler,
    chatgpt_handler,
    WAIT_TIME_AFTER_PROMPT_SHORT,
    WAIT_TIME_AFTER_PROMPT_LONG,
)
chatgpt_content_generator = ChatGPTContentGenerator(
    edge_handler,
    keyboard_handler,
    chatgpt_handler,
    prompt_generator,
    text_processor,
    WAIT_TIME_AFTER_RELOAD,
    WAIT_TIME_AFTER_PROMPT_SHORT,
    WAIT_TIME_AFTER_PROMPT_LONG,
)

json_processor = JSONProcessor()
formatter = Formatter()

# Excelファイルを読み込み、列情報を事前に取得
wb, ws = excel_handler.load_excel()
if not wb or not ws:
    print("Failed to load Excel workbook.")
    exit()

# 各列のインデックスを取得
column_indices = {
    "flag": excel_handler.find_matching_index(1, "flag", is_row_flag=True),
    "theme": excel_handler.find_matching_index(1, "theme", is_row_flag=True),
    "heading_suggestions": excel_handler.find_matching_index(
        1, "heading_suggestions", is_row_flag=True
    ),
    "heading": excel_handler.find_matching_index(1, "heading", is_row_flag=True),
}


def get_heading(group, start_row, column_indices):
    """"""
    first_row = int(group.index[0]) + 2

    flag = get_flag(excel_handler, first_row, column_indices)
    theme = get_theme(excel_handler, first_row, column_indices)

    if not check_flag_and_theme(flag, theme, first_row):
        logger.warning("Flag and theme check failed")
        return

    # 見出しの抽出（extract_heading メソッドを使用）
    heading_results = google_analyzer.extract_heading(theme)

    # Excelに保存する処理
    results_str = []
    target_index = start_row + 2
    for i, heading_result in enumerate(heading_results[:10], 1):
        result_data = {
            "url": heading_result["url"],
            "h2": heading_result["h2"],
            "h3": heading_result["h3"],
        }
        result_str = formatter.format_heading_result(result_data)

        excel_handler.update_cell(
            row=target_index,
            column=column_indices["heading_suggestions"],
            value=result_str,
        )
        results_str.append(result_str)
        target_index += 1
        if i == 10:
            break

    combined_results = "\n".join(results_str)
    combined_results = HEADING_PROMPT + "\n" + combined_results
    edge_handler.open_url_in_browser(CHATGPT_PATH)
    heading = chatgpt_content_generator.get_heading(combined_results)
    excel_handler.update_cell(
        row=start_row + 2,
        column=column_indices["heading"],
        value=heading,
    )
    excel_handler.save_to_excel()

# グループごとに処理を実行
grouped = pd.read_excel(EXCEL_FILE_PATH).groupby(lambda idx: idx // GROUP_SIZE)

for i, (_, group) in enumerate(grouped):
    start_row = i * GROUP_SIZE
    print(f"\nProcessing group starting at row {start_row}")
    get_heading(group, start_row, column_indices)

print("\nAll prompts have been processed and results saved to Excel.")
