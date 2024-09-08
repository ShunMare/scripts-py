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
GROUP_SIZE = 10

import pandas as pd
from handlers.excel_handler import ExcelHandler
from utils.data_retriever import (
    get_flag,
    get_theme,
    check_flag_and_theme,
)
from analyzers.google_search_analyzer import GoogleSearchAnalyzer

# 各種ハンドラーのインスタンスを作成
excel_handler = ExcelHandler(EXCEL_FILE_PATH)
google_analyzer = GoogleSearchAnalyzer()

# Excelファイルを読み込み、列情報を事前に取得
wb, ws = excel_handler.load_excel()
if not wb or not ws:
    print("Failed to load Excel workbook.")
    exit()

# 各列のインデックスを取得
column_indices = {
    "flag": excel_handler.find_matching_index(1, "flag", is_row_flag=True),
    "theme_suggestions": excel_handler.find_matching_index(
        1, "theme_suggestions", is_row_flag=True
    ),
    "theme": excel_handler.find_matching_index(1, "theme", is_row_flag=True),
    "heading_suggestions": excel_handler.find_matching_index(
        1, "heading_suggestions", is_row_flag=True
    ),
    "heading": excel_handler.find_matching_index(1, "heading", is_row_flag=True),
}


def get_themes(group, start_row, column_indices):
    """"""
    first_row = int(group.index[0]) + 2

    logger.debug(f"Column indices: {column_indices}")
    flag = get_flag(excel_handler, first_row, column_indices)
    theme = get_theme(excel_handler, first_row, column_indices)
    logger.debug(f"Flag: {flag}, Theme: {theme}")

    if not check_flag_and_theme(flag, theme, first_row):
        logger.warning("Flag and theme check failed")
        return

    # 関連キーワードの取得
    related_keywords = google_analyzer.get_related_keyword(theme)
    google_analyzer.print_related_keywords(theme, related_keywords)

    # Excelに保存する処理
    target_index = start_row + 2
    for i, related_keyword in enumerate(related_keywords[:10], 1):
        excel_handler.update_cell(
            row=target_index,
            column=column_indices["theme_suggestions"],
            value=related_keyword,
        )
        target_index += 1
        if i == 10:
            break
    excel_handler.save_to_excel()


# グループごとに処理を実行
grouped = pd.read_excel(EXCEL_FILE_PATH).groupby(lambda idx: idx // GROUP_SIZE)

for i, (_, group) in enumerate(grouped):
    start_row = i * GROUP_SIZE
    print(f"\nProcessing group starting at row {start_row}")
    get_themes(group, start_row, column_indices)

print("\nAll prompts have been processed and results saved to Excel.")
