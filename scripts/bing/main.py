import os
import sys
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
sys.path.append(project_root)


# 環境変数を取得し、デフォルト値を設定
load_dotenv(dotenv_path, override=True)
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "")
WAIT_TIME_AFTER_PROMPT_LONG = int(os.getenv("WAIT_TIME_AFTER_PROMPT_LONG", 200))
WAIT_TIME_AFTER_PROMPT_SHORT = int(os.getenv("WAIT_TIME_AFTER_PROMPT_SHORT", 100))
WAIT_TIME_AFTER_RELOAD = int(os.getenv("WAIT_TIME_AFTER_RELOAD", 5))
WAIT_TIME_AFTER_SWITCH = int(os.getenv("WAIT_TIME_AFTER_SWITCH", 3))
SHORT_WAIT_TIME = float(os.getenv("SHORT_WAIT_TIME", 0.5))
BING_PATH = os.getenv("BING_PATH", "https://www.bing.com/chat?form=NTPCHB")
EDGE_DRIVER_PATH = os.getenv("EDGE_DRIVER_PATH", "")
GROUP_SIZE = 10

import pandas as pd
from handlers.excel_handler import ExcelHandler
from handlers.edge_handler import EdgeHandler
from handlers.keyboard_handler import KeyboardHandler
from handlers.bing_handler import BingHandler
from generators.prompt_generator import PromptGenerator
from utils.data_retriever import (
    get_flag,
    get_theme,
    get_directions,
    check_flag_and_directions,
)
from generators.bing_content_generator import BingContentGenerator

# 各種ハンドラーのインスタンスを作成
excel_handler = ExcelHandler(EXCEL_FILE_PATH)
edge_handler = EdgeHandler(
    driver_path=EDGE_DRIVER_PATH,
    wait_time_after_switch=WAIT_TIME_AFTER_SWITCH,
)
keyboard_handler = KeyboardHandler(short_wait_time=SHORT_WAIT_TIME)
bing_handler = BingHandler(
    edge_handler,
    keyboard_handler,
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
)
prompt_generator = PromptGenerator(
    keyboard_handler,
    bing_handler,
    WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
)
bing_content_generator = BingContentGenerator(
    edge_handler=edge_handler,
    keyboard_handler=keyboard_handler,
    bing_handler=bing_handler,
    prompt_generator=prompt_generator,
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
)

# Excelファイルを読み込み、列情報を事前に取得
wb, ws = excel_handler.load_excel()
if not wb or not ws:
    print("Failed to load Excel workbook.")
    exit()

# 各列のインデックスを取得
column_indices = {
    "flag": excel_handler.find_matching_index(1, "flag", is_row_flag=True),
    "theme": excel_handler.find_matching_index(1, "theme", is_row_flag=True),
    "direction": excel_handler.find_matching_index(1, "direction", is_row_flag=True),
    "evidence": excel_handler.find_matching_index(1, "evidence", is_row_flag=True),
}


# データ処理関数
def generate_and_process_prompts(group, start_row, column_indices):
    """指定されたグループのプロンプトを生成し、処理する"""
    edge_handler.open_url_in_browser(BING_PATH)
    first_row = int(group.index[0]) + 2

    flag = get_flag(excel_handler, first_row, column_indices)
    theme = get_theme(excel_handler, first_row, column_indices)
    directions = get_directions(excel_handler, column_indices, group)
    if not check_flag_and_directions(flag, directions, first_row):
        return

    for direction in directions:
        bing_content_generator.send_evidence(
            theme=theme, direction=direction, isFirst=True
        )


# グループごとに処理を実行
grouped = pd.read_excel(EXCEL_FILE_PATH).groupby(lambda idx: idx // GROUP_SIZE)


for i, (_, group) in enumerate(grouped):
    start_row = i * GROUP_SIZE
    print(f"\nProcessing group starting at row {start_row}")
    generate_and_process_prompts(group, start_row, column_indices)

print("\nAll prompts have been processed and results saved to Excel.")
